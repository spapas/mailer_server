curl -v -H "Content-Type: multipart/form-data" ^
 -H "Authorization: Token da474acd50a6485a93ac5be434d2848af8119464" ^
 -X POST -F mail_to=spapas@hcg.gr -F subject=world -F body="hello world"  -F attachment=@massapicall.txt -F attachment=@apicall.txt ^
 http://127.0.0.1:8005/mail/api/send_mail/
