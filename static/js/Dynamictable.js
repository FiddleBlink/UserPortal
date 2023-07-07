var userList = [] 

$("#ShowUsers").click(function () {
    const tableBody = document.getElementById("TableOfUsers");
    tableBody.innerHTML = "";    //Everytime the show users button is clicked this script will run
    getusers();     
});

function getusers() {       //this is getting all the users in the database in JSON format
    console.log("Getting data from server...");
    $.ajax({
        url: "/getusers/",
        type: "GET",
        success: function (response) {
            userList = JSON.parse(response);        //parsing the JSON data so the we can actually use it 
            renderUserTable();
        },
    });
}

function renderUserTable() {        //this creates a entire body of the users table to show all users dynamically
    console.log("in render table")
    const tableBody = document.getElementById("TableOfUsers");
    userList.forEach(function (user, index) {       //for every user this function will add a new row with thier filled data
        user = user.fields;
        const row = tableBody.insertRow();          //this will create a new row in the table body

        const count = document.createElement("td");         //we create a new element td and assign it to count
        count.innerHTML = index + 1;                        //we change the innerHTML of count
        const name = document.createElement("td");          //we create a new element td and assign it to name
        name.innerHTML = user.first_name;                   //we change the innerHTML of name to the users name
        const email = document.createElement("td");
        email.innerHTML = user.email;
        const birthyear = document.createElement("td");
        birthyear.innerHTML = user.birth_year;
        const visibility = document.createElement("td");
        visibility.innerHTML = user.public_visibility;
        const dept = document.createElement("td");
        dept.innerHTML = user.department;
        const desig = document.createElement("td");
        desig.innerHTML = user.designation;
        const manager = document.createElement("td");
        manager.innerHTML = user.manager;
        const address = document.createElement("td");
        address.innerHTML = user.address;

        const pic = document.createElement("td");       //here we create a new td tag and assign to pic
        const img = document.createElement("img");      //we create a new img tag and assign to img
        img.src = "/images/" + user.profilepic;         //we set the source of the img tag to users profilepic url
        img.style.width = "100px";
        img.style.height = "auto";
        pic.appendChild(img);                           //we insert the img tag inside the td tag 

        row.appendChild(count);                         //then we insert the respective colums in the row of the table
        row.appendChild(name);
        row.appendChild(email);
        row.appendChild(birthyear);
        row.appendChild(visibility);
        row.appendChild(dept);
        row.appendChild(desig);
        row.appendChild(manager);
        row.appendChild(address);
        row.appendChild(pic);
    })
}