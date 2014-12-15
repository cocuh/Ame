#プログラミング言語 Ame
Esolangも言語系もよく知らない私が深いこと考えないで行きあたりばったりで作った言語です。  
作ってからそれとなく「Whitespaceに似てるなぁ」とか思ったのは内緒です。  

Ameという名前の由来は見た目。
```
/  //  ../   ./  . /|   /
/  /| |  /  //  |   |/|  /| 
|. /||  |/  |/  |  |/.  /| 
|/  /  /|  ||/.   /|/.  
/|   ＿＿,＿＿  / /.  /|
 / ／　／　 　＼　＼| / |/
　　^^^^^^ｌ^^^^^^   /!  ./
　雨だね。　ｌ∧＿∧　　 /!..
  傘いるかいｌ´･ω･｀)　
　　　　　　０⊂ 　　) 　
　　　　　　 　し─Ｊ  　 
```

[解説ブログ](http://cocu.hatenablog.com/entry/2012/12/05/000000)

##特徴
1. 多分スタック指向  
多分というのは、スタックが2つ(WM,LTM)と変数(tmp)があるため。  
これはswapが文法上難しかったための代替手段。2番目のスタックを変数にpullできるpull2コマンドと、他のデータの保管用のスタックがもう一つあるためこれでswapできる。  
そのこともあり、演算結果はpushされずにtmpに代入される  
2. 3進数で表現  
2進数だと長い。なるべく少ない文字数で難読に作りたい。よって3進数。  
3. 4文字使用(他はスペース含めコメント)  
使う文字:/|.!  

##語彙
###数値宣言  
"/"と"!"の間に3進数で記入。  
ただし、最高位は右側。
{0:/, 1:|, 2:.} 
```
////|!:27
/...!:26
```
###コマンドなど  
<table border="2">
<tr><td>command</td><td>meaning</td>
<th rowspan="10" width="30"></th><td>command</td><td>meaning</td><td>example</td>
</tr>
<tr><td>.//</td><td>WM.push</td><td>!//</td><td>+</td><td>WM[1]+WM[0]</td>
</tr>
<tr><td>.|/</td><td>WM.pull</td><td>!|/</td><td>-</td><td>WM[1]-WM[0]</td>
</tr>
<tr><td>../</td><td>WM.pull2</td><td>!./</td><td>&lowast;</td><td>WM[1]&lowast;WM[0]</td>
</tr>
<tr><td>./|</td><td>LTM.push</td><td>!/|</td><td>/</td><td>WM[1]/WM[0]</td>
</tr>
<tr><td>.||</td><td>LTM.pull</td><td>!||</td><td>%</td><td>WM[1]%WM[0]</td>
</tr>
<tr><td>..|</td><td>LTM.pull2</td><td>!.|</td><td>&lt;</td><td>1 if WM[1]&lt;WM[0] else 0</td>
</tr>
<tr><td>./.</td><td>WM.top</td><td>!/.</td><td>if</td><td>if WM[0]==0:</td>
</tr>
<tr><td>.|.</td><td>LTM.top</td><td>!|.</td><td>while</td><td>while WM[0]!=0:</td>
</tr>
<tr><td>...</td><td>loop,ifの終わりEnd</td><td>!..</td><td>print</td><td>print(str(WM[0]),end='')</td>
</tr>
</table>

すべてWM上の操作で演算後はpushされずにtmpに代入される

####str()とは

3進数で5桁区切りでASCIIコードに変換する

##開発環境
Python2.7で組みましたが、Python3.xでも動くようにしてあります。  
難読言語だしコードも難読じゃないとと思ってワンライナーで書きました。
```
Python 2.7.3
Arch Linux
```
