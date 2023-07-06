var userList = [] 
$("#ShowUsers").click(function () {
    getusers();
});

function getusers() {
    console.log("Getting data from server...");
    $.ajax({
        url: "/getusers/",
        type: "GET",
        success: function (response) {
            userList = JSON.parse(response);
            renderUserTable();
        },
    });
}

function renderUserTable() {
    console.log("in render table")
    const tableBody = document.getElementById("TableOfUsers");
    userList.forEach(function (user, index) {
        user = user.fields
        const row = tableBody.insertRow()

        const count = document.createElement("td")
        count.innerHTML = index + 1
        const name = document.createElement("td")
        name.innerHTML = user.first_name
        const email = document.createElement("td")
        email.innerHTML = user.email
        const birthyear = document.createElement("td")
        birthyear.innerHTML = user.birth_year
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
        const pic = document.createElement("td");
        const img = document.createElement("img");
        img.src = '/images/' + user.profilepic;
        img.style.width = '100px';
        img.style.height = 'auto';
        pic.appendChild(img)
        row.appendChild(count)
        row.appendChild(name)
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
// $(document).ready(function () {
//     console.log("working");
// });
