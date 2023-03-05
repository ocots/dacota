function perform_compound_search() {
  // Get the input field and table
  let filterInput = document.getElementById("compound-filter");
  let table = document.getElementById("compound-table");

  // Add event listener for input
  filterInput.addEventListener("keyup", function () {
    let filterValue = filterInput.value.toLowerCase();

    // Loop through table rows
    for (let i = 1; i < table.rows.length; i++) {
      let row = table.rows[i];
      let name = row.cells[1].innerText.toLowerCase();

      if (name.indexOf(filterValue) > -1) {
        row.style.display = "";
      } else {
        row.style.display = "none";
      }
    }
  });
}

function perform_search() {
  var input, filter, table1, table2, tr, td1, td2, i, txtValue;
  input = document.getElementById("search");
  filter = input.value.toUpperCase();
  table1 = document.getElementById("compound-table");
  table2 = document.getElementById("binary-relations-table");
  tr1 = table1.getElementsByTagName("tr");
  tr2 = table2.getElementsByTagName("tr");
  for (i = 0; i < tr1.length; i++) {
    td1 = tr1[i].getElementsByTagName("td")[1];
    if (td1) {
      txtValue = td1.textContent || td1.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr1[i].style.display = "";
      } else {
        tr1[i].style.display = "none";
      }
    }
  }
  for (i = 0; i < tr2.length; i++) {
    td1 = tr2[i].getElementsByTagName("td")[1];
    td2 = tr2[i].getElementsByTagName("td")[2];
    if (td1 || td2) {
      txtValue1 = td1.textContent || td1.innerText;
      txtValue2 = td2.textContent || td2.innerText;
      if (
        txtValue1.toUpperCase().indexOf(filter) > -1 ||
        txtValue2.toUpperCase().indexOf(filter) > -1
      ) {
        tr2[i].style.display = "";
      } else {
        tr2[i].style.display = "none";
      }
    }
  }
}

function perform_binary_relations_search() {
  var input, filter, table, tr, td1, td2, i, txtValue1, txtValue2;
  input = document.getElementById("binary-relations-search");
  filter = input.value.toUpperCase();
  table = document.getElementById("binary-relations-table");
  tr = table.getElementsByTagName("tr");
  for (i = 0; i < tr.length; i++) {
    td1 = tr[i].getElementsByTagName("td")[1];
    td2 = tr[i].getElementsByTagName("td")[2];
    if (td1 || td2) {
      txtValue1 = td1.textContent || td1.innerText;
      txtValue2 = td2.textContent || td2.innerText;
      if (
        txtValue1.toUpperCase().indexOf(filter) > -1 ||
        txtValue2.toUpperCase().indexOf(filter) > -1
      ) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
}

//delete compound
function Delete(id, name) {
  if (window.confirm("Are you sure you want to delete " + name)) {
    var path = "delete_compound/" + id;
    document.location.href = path;
  }
}

function Delete_relation(id, name1, name2) {
  if (
    window.confirm(
      "Are you sure you want to delete the relation " +
      name1 +
      "-" +
      name2
    )
  ) {
    var path = "delete_relation/" + id;
    document.location.href = path;
  }
}

const component_keys = ["id", "name", "a", "b", "c"];
const relation_keys = ["id", "component1", "component2", "a12", "a21", "alpha"];
var originalValuesComponent = new Map();
var originalValuesRelation = new Map();

function toggleEdit(rowId) {
  let row = document.getElementById(rowId);
  const data = {}
  let cells = row.getElementsByTagName("td");
  var keys;

  if (rowId.startsWith("component")) {
    keys = component_keys;
  } else {
    keys = relation_keys;
  }

  var buttons = row.getElementsByTagName("i");
  var edit = cells[1].getAttribute("editable") === 'false' || cells[1].getAttribute("editable") === null;
  if (edit) {
    buttons[0].style.display = "none";
    buttons[3].style.display = "none";
    buttons[1].style.display = "inline-block";
    buttons[2].style.display = "inline-block";
  }




  for (let i = 0; i < cells.length - 1; i++) {
    if (cells[i].getAttribute("editable") === 'false' || cells[i].getAttribute("editable") === null) {
      if (cells[i].getAttribute("noneditable") === "true") {
        data[keys[i]] = cells[i].innerHTML;
        continue;
      }
      data[keys[i]] = cells[i].innerHTML;
      let input = document.createElement("input");
      input.type = "text";
      input.value = cells[i].innerHTML;
      input.style.width = cells[i].offsetWidth + "px";
      cells[i].innerHTML = "";
      cells[i].appendChild(input);
      cells[i].setAttribute("editable", "true");
      data[keys[i]]
    }
    else {
      if (cells[i].getAttribute("noneditable") === "true") continue;
      cells[i].setAttribute("editable", "false");
      let input = cells[i].querySelector("input");
      cells[i].innerHTML = `${input.value}`;
      data[keys[i]] = input.value;
    }
  }
  if (rowId.startsWith("component")) {
    originalValuesComponent.set(rowId, data);
  } else {
    originalValuesRelation.set(rowId, data);
  }
}

function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function saveChanges(rowId) {
  row = document.getElementById(rowId);
  var keys;

  var buttons = row.getElementsByTagName("i");
  buttons[0].style.display = "inline-block";
  buttons[1].style.display = "none";
  buttons[2].style.display = "none";
  buttons[3].style.display = "inline-block";



  if (rowId.startsWith("component")) {
    keys = component_keys;
  } else {
    keys = relation_keys;
  }
  data = {}
  var cells = row.getElementsByTagName("td");
  var csrftoken = getCookie('csrftoken');

  for (var j = 0; j < cells.length - 1; j++) {
    var input = cells[j].querySelector("input");
    if (input) {
      data[keys[j]] = input.value;
      this.toggleEdit(rowId);
    }
    else {
      data[keys[j]] = cells[j].innerHTML;
    }
  }
  console.log("data", data) // FORM OF THE DATA
  var headers = new Headers();
  headers.append('Content-Type', 'application/json');
  headers.append('X-CSRFToken', csrftoken);

  fetch("edit_" + rowId.split("-")[0], {
    method: 'POST',
    headers: headers,
    body: JSON.stringify(data),
  });
}

function cancelChanges(rowId) {
  var row = document.getElementById(rowId);
  var keys, originalValues;

  var buttons = row.getElementsByTagName("i");
  buttons[0].style.display = "inline-block";
  buttons[1].style.display = "none";
  buttons[2].style.display = "none";
  buttons[3].style.display = "inline-block";

  if (rowId.startsWith("component")) {
    keys = component_keys;
    originalValues = originalValuesComponent;
  } else {
    keys = relation_keys;
    originalValues = originalValuesRelation;
  }

  console.log(originalValues);
  let cells = row.getElementsByTagName("td");
  let editable = cells[1].getAttribute("editable");
  for (let i = 0; i < cells.length - 1; i++) {
    if (editable === "true") {
      let input = cells[i].querySelector("input");
      if (input) input.value = originalValues.get(rowId)[keys[i]];
    }
  }
  if (editable === "true") toggleEdit(rowId);
}
