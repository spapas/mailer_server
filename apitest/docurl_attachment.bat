curl -v -H "Content-Type: multipart/form-data" ^
 -H "Authorization: Token efb50ddb2fe1ff56fbe5804ed89e9733f9cf1099" ^
 -X POST -F mail_to=spapas@gmail.com -F subject=world -F body="hello world"  -F attachment=@massapicall.txt ^
 http://mlrsrv.hcg.gr/mail/api/send_mail/
