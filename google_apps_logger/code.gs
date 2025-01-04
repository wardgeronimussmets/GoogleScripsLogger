function doPost(e) {
  // Parse the request payload
  const data = JSON.parse(e.postData.contents);
  const spread_sheet_id = data.spread_sheet_id;
  if(!spread_sheet_id){
    return ContentService.createTextOutput("Spread sheet id is not set").setMimeType(ContentService.MimeType.TEXT);
  }
  const sheet = SpreadsheetApp.openById().getSheetByName("logs");

  // Append log data to the sheet
  sheet.appendRow([data.timestamp, data.logLevel, data.message]);

  return ContentService.createTextOutput("Log received").setMimeType(ContentService.MimeType.TEXT);
}
