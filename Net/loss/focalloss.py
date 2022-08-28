# Loss functions

import torch
import torch.nn as nn

from utils.metrics import bbox_iou
from utils.torch_utils import is_parallel
from torchvision.ops import RoIAlign


def smooth_BCE(eps=0.1):  # https://github.com/ultralytics/yolov3/issues/238#issuecomment-598028441
    # return positive, negative label smoothing BCE targets
    return 1.0 - 0.5 * eps, 0.5 * eps


class BCEBlurWithLogitsLoss(nn.Module):
    # BCEwithLogitLoss() with reduced missing label effects.
    def __init__(self, alpha=0.05):
        super(BCEBlurWithLogitsLoss, self).__init__()
        self.loss_fcn = nn.BCEWithLogitsLoss(reduction='none')  # must be nn.BCEWithLogitsLoss()
        self.alpha = alpha

    def forward(self, pred, true):
        loss = self.loss_fcn(pred, true)
        pred = torch.sigmoid(pred)  # prob from logits
        dx = pred - true  # reduce only missing label effects
        # dx = (pred - true).abs()  # reduce missing label and false label effects
        alpha_factor = 1 - torch.exp((dx - 1) / (self.alpha + 1e-4))
        loss *= alpha_factor
        return loss.mean()


class FocalLoss(nn.Module):
    # Wraps focal loss around existing loss_fcn(), i.e. criteria = FocalLoss(nn.BCEWithLogitsLoss(), gamma=1.5)
    def __init__(self, loss_fcn, gamma=1.5, alpha=0.25):
        super(FocalLoss, self).__init__()
        self.loss_fcn = loss_fcn  # must be nn.BCEWithLogitsLoss()
        self.gamma = gamma
        self.alpha = alpha
        self.reduction = loss_fcn.reduction
        self.loss_fcn.reduction = 'none'  # required to apply FL to each element

    def forward(self, pred, true):
        loss = self.loss_fcn(pred, true)
        # p_t = torch.exp(-loss)
        # loss *= self.alpha * (1.000001 - p_t) ** self.gamma  # non-zero power for gradient stability

        # TF implementation https://github.com/tensorflow/addons/blob/v0.7.1/tensorflow_addons/losses/focal_loss.py
        pred_prob = torch.sigmoid(pred)  # prob from logits
        p_t = true * pred_prob + (1 - true) * (1 - pred_prob)
        alpha_factor = true * self.alpha + (1 - true) * (1 - self.alpha)
        modulating_factor = (1.0 - p_t) ** self.gamma
        loss *= alpha_factor * modulating_factor

        if self.reduction == 'mean':
            return loss.mean()
        elif self.reduction == 'sum':
            return loss.sum()
        else:  # 'none'
            return loss


class QFocalLoss(nn.Module):
    # Wraps Quality focal loss around existing loss_fcn(), i.e. criteria = FocalLoss(nn.BCEWithLogitsLoss(), gamma=1.5)
    def __init__(self, loss_fcn, gamma=1.5, alpha=0.25):
        super(QFocalLoss, self).__init__()
        self.loss_fcn = loss_fcn  # must be nn.BCEWithLogitsLoss()
        self.gamma = gamma
        self.alpha = alpha
        self.reduction = loss_fcn.reduction
        self.loss_fcn.reduction = 'none'  # required to apply FL to each element

    def forward(self, pred, true):
        loss = self.loss_fcn(pred, true)

        pred_prob = torch.sigmoid(pred)  # prob from logits
        alpha_factor = true * self.alpha + (1 - true) * (1 - self.alpha)
        modulating_factor = torch.abs(true - pred_prob) ** self.gamma
        loss *= alpha_factor * modulating_factor

        if self.reduction == 'mean':
            return loss.mean()
        elif self.reduction == 'sum':
            return loss.sum()
        else:  # 'none'
            return loss


class ComputeLoss:
    # Compute losses
    def __init__(self, model, autobalance=False):
        super(ComputeLoss, self).__init__()
        self.sort_obj_iou = False
        device = next(model.parameters()).device  # get model device
        h = model.hyp  # hyperparameters

        # Define criteria
        BCEcls = nn.BCEWithLogitsLoss(pos_weight=torch.tensor([h['cls_pw']], device=device))
        BCEobj = nn.BCEWithLogitsLoss(pos_weight=torch.tensor([h['obj_pw']], device=device))

        # Class label smoothing https://arxiv.org/pdf/1902.04103.pdf eqn 3
        self.cp, self.cn = smooth_BCE(eps=h.get('label_smoothing', 0.0))  # positive, negative BCE targets

        # Focal loss
        g = h['fl_gamma']  # focal loss gamma
        if g > 0:
            BCEcls, BCEobj = FocalLoss(BCEcls, g), FocalLoss(BCEobj, g)

        det = model.module.model[-1] if is_parallel(model) else model.model[-1]  # Detect() module
        self.balance = {3: [4.0, 1.0, 0.4]}.get(det.nl, [4.0, 1.0, 0.25, 0.06, .02])  # P3-P7
        self.ssi = list(det.stride).index(16) if autobalance else 0  # stride 16 index
        self.BCEcls, self.BCEobj, self.gr, self.hyp, self.autobalance = BCEcls, BCEobj, model.gr, h, autobalance
        for k in 'na', 'nc', 'nl', 'anchors', 'stride':
            setattr(self, k, getattr(det, k))

    def __call__(self, p, targets, sml_flag = False):  # predictions, targets, model
        device = targets.device
        lcls, lbox, lobj = torch.zeros(1, device=device), torch.zeros(1, device=device), torch.zeros(1, device=device)
        lsml = torch.zeros(1, device=device)
        tcls, tbox, indices, anchors = self.build_targets(p, targets)  # targets
        if sml_flag:
            feature_h, feature_w = p[1].shape[2:4]
            img_h = feature_h * self.stride[1].item()
            img_w = feature_w * self.stride[1].item()
            image_shape = [(img_h,img_w)]
            lsml += self.SML_loss(p,targets,image_shape)

        # Losses
        for i, pi in enumerate(p[:2]):  # 遍历每个检测层和这一层上的预测结果，i:第几个检测层，pi:shape(bs, anchor数目, feature_w, feature_h,xywh, xywh置信度+类别数) # layer index, layer predictions
            b, a, gj, gi = indices[i]   # image, anchor, gridy, gridx, indices包含了这一层上所有正样本所在的batch的第几张图片上，是3个anchor的第几个，以及特征图上的第几个点
            tobj = torch.zeros_like(pi[..., 0], device=device)  # target obj

            n = b.shape[0]  # number of targets
            if n:
                ps = pi[b, a, gj, gi]  # prediction subset corresponding to targets, 获取特征图上对应目标位置的预测值-每个预测值6个数据，对应0:3 xywh，4 obj_conf，5及以后cls_prob

                # Regression
                pxy = ps[:, :2].sigmoid() * 2. - 0.5 # 获取预测的xy值
                pwh = (ps[:, 2:4].sigmoid() * 2) ** 2 * anchors[i] # 获取预测的wh值
                pbox = torch.cat((pxy, pwh), 1)  # predicted box 预测框的xywh值
                iou = bbox_iou(pbox.T, tbox[i], x1y1x2y2=False, CIoU=True)  # iou(prediction, target) 计算预测框pbox和tbox(GT)的IOU损失,默认采用CIOU
                lbox += (1.0 - iou).mean()  # iou loss

                # Objectness
                score_iou = iou.detach().clamp(0).type(tobj.dtype)
                if self.sort_obj_iou:
                    sort_id = torch.argsort(score_iou)
                    b, a, gj, gi, score_iou = b[sort_id], a[sort_id], gj[sort_id], gi[sort_id], score_iou[sort_id]
                tobj[b, a, gj, gi] = (1.0 - self.gr) + self.gr * score_iou  # iou ratio

                # Classification
                if self.nc > 1:  # cls loss (only if multiple classes)
                    t = torch.full_like(ps[:, 5:], self.cn, device=device)  # targets
                    t[range(n), tcls[i]] = self.cp
                    lcls += self.BCEcls(ps[:, 5:], t)  # BCE

                # Append targets to text file
                # with open('targets.txt', 'a') as file:
                #     [file.write('%11.5g ' * 4 % tuple(x) + '\n') for x in torch.cat((txy[i], twh[i]), 1)]

            obji = self.BCEobj(pi[..., 4], tobj)
            lobj += obji * self.balance[i]  # obj loss
            if self.autobalance:
                self.balance[i] = self.balance[i] * 0.9999 + 0.0001 / obji.detach().item()

        if self.autobalance:
            self.balance = [x / self.balance[self.ssi] for x in self.balance]
        lbox *= self.hyp['box']
        lobj *= self.hyp['obj']
        lcls *= self.hyp['cls']
        bs = tobj.shape[0]  # batch size
        if sml_flag:
            loss = lbox + lobj + lcls + lsml
            return loss * bs, torch.cat((lbox, lobj, lcls, lsml, loss)).detach()
        else:
            loss = lbox + lobj + lcls
            return loss * bs, torch.cat((lbox, lobj, lcls, loss)).detach()

    def build_targets(self, p, targets):
        # Build targets for compute_loss(), input targets(image,class,x,y,w,h)
        na, nt = self.na, targets.shape[0]  # number of anchors, targets
        tcls, tbox, indices, anch = [], [], [], []
        gain = torch.ones(7, device=targets.device)  # normalized to gridspace gain
        # torch.arange()函数为等间隔生成一段序列 如 torch.arange(3)的结果为[0,1,2] tensor.float()为将结果转换为浮点数
        # tensor.view(na,1)此处为将一维tensor的行转换为列且升维为二维tensor
        # tensor.repeat(1,nt)此处为每一行重复第一个元素重复nt次 因此最终的ai尺寸为[na,nt]
        ai = torch.arange(na, device=targets.device).float().view(na, 1).repeat(1, nt)  # same as .repeat_interleave(nt) shape[3,34]
        # tensor.repeat(na,1,1)将原始一维向量在第1/2/3个维度上分别重复 na,1,1次 ai[:,:,None]将原二维tensor ai扩充至三维 且第三维为1
        # tensor.cat(tensor1,tensor2,2) 将两个三维tensor在第三个维度上面拼接到了一起
        # tensor1[1*na,nt*1,1]和tensor2[na,nt,1]的张量的第三维cat一起之后 为[na,nt,2]
        targets = torch.cat((targets.repeat(na, 1, 1), ai[:, :, None]), 2)  # append anchor indices ,shape[3,34,7]

        g = 0.5  # bias
        off = torch.tensor([[0, 0],
                            [1, 0], [0, 1], [-1, 0], [0, -1],  # j,k,l,m
                            # [1, 1], [1, -1], [-1, 1], [-1, -1],  # jk,jm,lk,lm
                            ], device=targets.device).float() * g  # offsets
        # off是维度为[5, 2]的tensor,[[0, 0], [0.5, 0], [0, 0.5], [-0.5, 0]. [0, -0.5]]
        for i in range(self.nl):
            anchors = self.anchors[i]
            """
            p[i].shape = (b, 3, h, w，nc+5), hw分别为特征图的长宽
            gain = [1, 1, w, h, w, h, 1]
            """
            gain[2:6] = torch.tensor(p[i].shape)[[3, 2, 3, 2]]  # xyxy gain

            # Match targets to anchors
            t = targets * gain
            if nt:
                # Matches
                r = t[:, :, 4:6] / anchors[:, None]  # wh ratio , shape为(3,num_targets,2)
                j = torch.max(r, 1. / r).max(2)[0] < self.hyp['anchor_t']  # compare
                # j = wh_iou(anchors, t[:, 4:6]) > model.hyp['iou_t']  # iou(3,n)=wh_iou(anchors(3,2), gwh(n,2))
                t = t[j]  # filter
                # Offsets
                # 得到中心点坐标xy（相对于左上角）
                gxy = t[:, 2:4]  # grid xy
                # 得到中心点相当于右下角的坐标
                gxi = gain[[2, 3]] - gxy  # inverse
                j, k = ((gxy % 1. < g) & (gxy > 1.)).T
                l, m = ((gxi % 1. < g) & (gxi > 1.)).T
                j = torch.stack((torch.ones_like(j), j, k, l, m))
                t = t.repeat((5, 1, 1))[j]
                offsets = (torch.zeros_like(gxy)[None] + off[:, None])[j]
            else:
                t = targets[0]
                offsets = 0

            # Define
            b, c = t[:, :2].long().T  # image, class
            gxy = t[:, 2:4]  # grid xy
            gwh = t[:, 4:6]  # grid wh
            gij = (gxy - offsets).long()
            gi, gj = gij.T  # grid xy indices

            # Append
            a = t[:, 6].long()  # anchor indices
            indices.append((b, a, gj.clamp_(0, gain[3] - 1), gi.clamp_(0, gain[2] - 1)))  # image, anchor, grid indices
            tbox.append(torch.cat((gxy - gij, gwh), 1))  # box
            anch.append(anchors[a])  # anchors
            tcls.append(c)  # class

        return tcls, tbox, indices, anch

    def SML_loss(self,p,targets,image_shape):
        feature = p[-1]
        gain = torch.ones(6, device=targets.device)
        gain[2:] = torch.tensor(p[0].shape)[[3, 2, 3, 2]] * self.stride[0]
        t = targets * gain

        target_abs = t[:, 2:]
        target_abs[:, 0] = target_abs[:, 0] - target_abs[:, 2] / 2
        target_abs[:, 1] = target_abs[:, 1] - target_abs[:, 3] / 2
        target_abs[:, 2] = target_abs[:, 0] + target_abs[:, 2] / 2
        target_abs[:, 3] = target_abs[:, 1] + target_abs[:, 3] / 2

        j = (target_abs[:, 3] - target_abs[:, 1])>5

        large_target = target_abs[j]
        i = (target_abs[:, 3] - target_abs[:, 1])<5

        small_target = target_abs[i]

        roi_features_large = []
        roi_features_small = []

        distance = 0

        if len(large_target) and len(small_target):
            from torchvision.ops import MultiScaleRoIAlign
            box_roi_pool = MultiScaleRoIAlign(
                featmap_names=['0'],
                output_size = [7, 7],
                sampling_ratio=2)
            feature = {'0': feature}

            box_features_large = box_roi_pool(feature, [large_target], image_shape)
            roi_features_large.append(torch.flatten(box_features_large, start_dim=1))

            box_features_small = box_roi_pool(feature, [small_target], image_shape)
            roi_features_small.append(torch.flatten(box_features_small, start_dim=1))

            for i in range(roi_features_small[0].shape[0]):
                D_value = roi_features_small[0][i] - torch.mean(roi_features_large[0], dim=0)
                distance += torch.norm(D_value, dim=0) / roi_features_small[0].shape[1]

            return distance/roi_features_small[0].shape[0]
        else:
            return distance



