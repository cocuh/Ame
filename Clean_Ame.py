# vim: fileencoding=utf-8
import sys
import os
import subprocess as sp

if __name__ == '__main__':
    ####変数宣言####
    Usage = "Usage: Ame FILE [DEBUG]"
    DebugMode = 0
    DebugModeMessage='print("""#  WM:{WM}\n# LTM:{LTM}\n# ptr:{ptr} ptr_tmp:{len_ptr_tmp}:{ptr_tmp} depth:{source_depth}\n# tmp:{tmp} sourcelist:{len_sourcelist}:{sourcelist}\n""".format(WM=WM,LTM=LTM,tmp=tmp,len_sourcelist=len(sourcelist),sourcelist=sourcelist,ptr=ptr,len_ptr_tmp=len(ptr_tmp),source_depth=source_depth,ptr_tmp=ptr_tmp))'
    sourceraw = ''
    sourcelist = []
    filename = ''
    
    WM = []
    LTM = []
    ptr_tmp = []
        #ptr_tmp[n] = (ptr,if->0loop->1)
    source_depth = 0
    triggers = []
    ptr = 0
    tmp = 0

    ####関数宣言####
    substitution = lambda x,y:globals().__setitem__(x,y)
    substitution_tmp = lambda y:substitution('tmp',y)
    
    stack_delete_top = lambda m:substitution(m,globals()[m][1:])
    stack_delete_sec = lambda m:substitution(m,[globals()[m][0]]+globals()[m][2:])
    
    stdout = lambda x:sys.stdout.write(x)and 0

    def SyntaxError(errorname=''):
        print(':'.join(["SyntaxError",errorname]))
        print(sourceraw)
        print(sourcelist)
        sys.exit(0)

    parse_number=lambda x,y=0:parse_number(x[1:],y*3+{'/':0,'|':1,'.':2}[x[0]])if x else y

    exec_number=lambda x:substitution_tmp(parse_number(x[1:-1][::-1]))

    parse_string=lambda x,r=[]:parse_string(x//243,r+[x%243]) if x else r
    exec_string=lambda i:(''.join([chr(x)for x in parse_string(i)]))if sys.version_info[0]-3 else(str(bytes(parse_string(i)),"ascii"))
    ########



    #Usage表示
    if len(sys.argv) == 1:
        sys.exit(Usage)
    filename = sys.argv[1]


    #ファイル例外処理
    if not os.path.exists(filename):
        sys.exit("Not such file: " + filename)
    if not os.access(filename,os.R_OK):
        sys.exit("Can't read this file: " + filename)
    
    #不要文字処理
    if(len(sys.argv) == 3 and sys.argv[2] == 'DEBUG'):
        DebugMode = 1
    sourceraw = ''.join(filter(lambda x:x in ['/','|','.','!'],open(filename).read()))

    #単語分解
    if DebugMode:
        print('##sourceraw: '+sourceraw)

    parser = lambda:(((substitution('sourcelist',sourcelist+[sourceraw[:3]])or substitution('sourceraw',sourceraw[3:]))if len(sourceraw)-2>0 else(SyntaxError()))if sourceraw[0]in'.!'else(((substitution('sourcelist',sourcelist+[sourceraw[:sourceraw.index('!')+1]])or substitution('sourceraw',sourceraw[sourceraw.index('!')+1:]))if '!'in sourceraw else(SyntaxError()))if sourceraw[0]in'/'else(SyntaxError())))if sourceraw else True

    while not parser():
        pass

    if DebugMode:
        print('##sourcelist: '+str(sourcelist))

    #深さチェック count('loop')+count('if') == '...'
    if len(list(filter(lambda i:i in['!/.','!|.'],sourcelist)))!=sourcelist.count('...'):
        SyntaxError('depth error:check "!/.", "!|." or "..."')

    #意味判定と実行

    dic_cmd={  './/':(lambda:substitution('WM',[tmp]+WM)or substitution_tmp(0)),
                '.|/':(lambda:substitution_tmp(WM[0])or stack_delete_top('WM')),
                '../':(lambda:substitution_tmp(WM[1])or stack_delete_sec('WM')),
                './|':(lambda:substitution('LTM',[tmp]+LTM)),
                '.||':(lambda:substitution_tmp(LTM[0])or stack_delete_top('LTM')),
                '..|':(lambda:substitution_tmp(LTM[1])or stack_delete_sec('LTM')),
                './.':(lambda:substitution_tmp(WM[0])),
                '.|.':(lambda:substitution_tmp(LTM[0])),
                '...':(lambda:substitution('source_depth',source_depth-1) or(_LOOP()if ptr_tmp[0][1]else _IF())),#end

                '!//':(lambda:substitution_tmp(WM[1]+WM[0])),
                '!|/':(lambda:substitution_tmp(WM[1]-WM[0])),
                '!./':(lambda:substitution_tmp(WM[1]*WM[0])),
                '!/|':(lambda:substitution_tmp(WM[1]//WM[0])),
                '!||':(lambda:substitution_tmp(WM[1]%WM[0])),
                '!.|':(lambda:substitution_tmp(1 if WM[1]<WM[0]else 0)),#<
                '!/.':(lambda:substitution('source_depth',source_depth+1)or(None if WM[0]else substitution('ptr_tmp',[(ptr,0)]+ptr_tmp))),#if == 0
                '!|.':(lambda:substitution('source_depth',source_depth+1)or(substitution('ptr_tmp',[(ptr,1)]+ptr_tmp)if WM[0]else None)),#loop != 0
                '!..':(lambda:(stdout(exec_string(WM[0]))or stack_delete_top('WM'))),#print
                }
    
    _IF = lambda:substitution('ptr_tmp',ptr_tmp[1:])
    _LOOP = lambda:substitution('ptr',ptr_tmp[0][0]-1)or substitution('ptr_tmp',ptr_tmp[1:])

    ptr = 0 
    def exec_source():
        global ptr
        global source_depth
        command = sourcelist[ptr]
        if len(ptr_tmp) == source_depth:
            if command[0]in'/':
                exec_number(command)
            else:
                dic_cmd[command]()
        else:
            if command in['!/.','!|.']:
                source_depth += 1
            elif command == '...':
                source_depth -= 1
        ptr += 1


    exec(DebugModeMessage if DebugMode else'')
    while ptr<len(sourcelist):
        if DebugMode:
            print('========='+sourcelist[ptr])
        exec_source()
        exec(DebugModeMessage if DebugMode else'')







