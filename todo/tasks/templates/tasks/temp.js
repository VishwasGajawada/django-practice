var editButtons = document.querySelectorAll('.edit-button');
var submitButtons = document.querySelectorAll('.submit-button');
function editClose(e){
    var parent = e.parentElement;
    console.log(parent);
}
function editOpen(e){
    
}
function changeEditStatus(e){
    // e.preventDefault();
    console.log("Opening ",e.id);
    if(e.innerHTML=="Edit"){
        editOpen(e);
    }else{
        editClose(e);
    }
}
for (const editButton of editButtons){
    editButton.addEventListener('click',()=>changeEditStatus(editButton));
}
for (const editButton of editButtons){
    editClose(editButton);
}