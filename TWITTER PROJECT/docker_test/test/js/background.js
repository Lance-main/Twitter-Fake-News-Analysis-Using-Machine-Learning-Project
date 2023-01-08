chrome.contextMenus.create ({    "title": "OSM fake content detection",    "contexts": ["selection"],    "onclick": openTab()});
var bkg = chrome.extension.getBackgroundPage();

function openTab(){    return function(info, tab){     
   let v = Math.random() * (3 - 0) + 0;
   let text = info.selectionText;
   let o = ["FAKE","SEEMS FAKE","CREDIBLE","SEEMS CREDIBLE"]
   
  
   function httpGet()
   {
       theUrl="http://127.0.0.1:8000/api/get/twitter/analysis?keyword="+text
       var xmlHttp = new XMLHttpRequest();
       xmlHttp.open("GET", theUrl, false ); // false for synchronous request
       xmlHttp.send(null);
       data = JSON.parse(xmlHttp.responseText)
       alert(o[data["data"]])
            //return xmlHttp.responseText;
   }

   httpGet();
   chrome.notifications.create('NOTFICATION_ID', {
    type: 'basic',
    iconUrl: 'path',
    title: 'notification title',
    message: 'notification message',
    priority: 1
})  

       // bkg.console.log(document.body.innerHTML)
       // bkg.console.log("helllllo")
       // chrome.tabs.create ({index: tab.index + 1, url: redditLink, selected: true});   
        }
    };



function format(subName){    

if (subName[0] === "r" && subName[1] === "/"){        
  return subName    
} 
   else { 
       return "r/" + subName  ;  }

};



