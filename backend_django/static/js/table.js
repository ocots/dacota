function perform_compound_search(){
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
