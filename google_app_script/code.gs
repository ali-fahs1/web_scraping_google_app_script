function opOpen(){
  const ui=SpreadsheetApp.getUi();
  ui.createMenu('send email').addItem('Approve','approver').addToUi() 


}
function approver(){
   
   const ui=SpreadsheetApp.getUi();
   const row=SpreadsheetApp.getActiveSheet().getActiveCell().getRow()
   const data=SpreadsheetApp.getActiveSheet().getRange(row,1,1,5).getValues()[0];
   const user={
      name:data[0],
      email:data[4],
      row:row  

   }
   const res=ui.alert('Send to '+user.name+' ('+user.email+')',ui.ButtonSet.YES_NO);
   if (res==ui.Button.YES){
          sendUser(user)

   }
   
}
function sendUser(user){
  const temp=HtmlService.createTemplateFromFile('temp');
  temp.user=user
  const message=temp.evaluate().getContent()

  MailApp.sendEmail({
    to:user.email,
    subject:'offer',
    htmlBody:message
  })
  SpreadsheetApp.getActiveSheet().getRange(user.row,6).setValue('sent')
}

