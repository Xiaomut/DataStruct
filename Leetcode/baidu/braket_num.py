import re

code = """
public class Test {
   public static void main(String[] args){
      int [] numbers = {10, 20, 30, 40, 50};

      for (int x : numbers ) {
         System.out.print( x );
         System.out.print(",");
      }
      System.out.print("\n");
      String [] names ={"James", "Larry", "Tom", "Lacy"};
      for ( String name : names ) {
         System.out.print( name );
         System.out.print(",");
         for () {
            asddasd;
         }

         for () {
            asddasd;
         }

      }
   }
}
"""

# brackets = re.search(".*?for.*?\) (.*?)\}\n", code)
# print(len(brackets))

# code = input()
for_dic = []
other_dic = []
res = 0
cur = 0
flag = False
for text in code.split("\n"):
    text = text.strip()
    print(text)
    if text.startswith("for") and text[3] == ' ' and flag is False:
        flag = True
        for_dic.append("{")
        cur = 1
    elif text.startswith("for") and text[3] == ' ' and flag is True:
        for_dic.append("{")
        cur += 1
    elif text.startswith("if") and text[2] == ' ':
        other_dic.append("{")
    elif text == '}':
        if other_dic:
            other_dic.pop()
        elif for_dic:
            for_dic.pop()
        if len(for_dic) == 0:
            res = max(res, cur)
            cur = 0
            flag = False
print(res)