
**Q:** `Why use MAE loss function instead of MSE?`
**A:** Outliers only represent data corruption or wrong sampling, so we don’t need to pay too much attention. That's why we choose MAE as the loss function.

**Q:** `How is the effect, did you only test three images?`
**A:** Not only tested three, only three images are shown here. The registration results of most images are similar to Elastix and better than ANTs. 


**Q:** `What is self-supervised learning?`
**A:** There are three most common paradigms in deep learning, supervised learning, unsupervised learning and semi-supervised learning. Among them, unsupervised learning is more difficult. Self-supervised learning mainly uses pretext, alse call auxiliary tasks, to mine its own supervised information from large-scale unsupervised data, and trains the network through this constructed supervised information, so that it can learn valuable representations for downstream tasks.
