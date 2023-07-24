/**
 * adding eventlisteners for drag and drop
 */
document.addEventListener("drop", dropHandler)
document.addEventListener("dragover", dragOverHandler)

/**
 * adding event listeners for adding new cuttingplan form
 */
document.querySelector('#add-cp')?.addEventListener("click", show_app_cp);
document.querySelector('#add-customer')?.addEventListener("click", show_add_customer);
document.querySelector('#hide-customer')?.addEventListener("click", hide_add_customer);
document.querySelector('#add-customer-group')?.addEventListener("click", show_add_customer_group);
document.querySelector('#hide-customer-group')?.addEventListener("click", hide_add_customer_group);


/**
 * Eventlistener for sidebar
 */
document.querySelector('#show_cuttingcode')?.addEventListener("click", getMachineCode)
document.querySelector('#show_cuttingdisplay')?.addEventListener("click", show_breakpic)
document.querySelector('#show-header')?.addEventListener("click", show_header_information)
document.querySelector('#download-edi')?.addEventListener("click", down_load_edi_file)

/**
 * gets the plain machine code for the cutting plan and switches the view
 * @returns early if display is alread active
 */
function getMachineCode() {
    if (!document.querySelector('#cuttingcode').hidden){
        return;
    }

    let id = document.querySelector('#pattern-id').innerHTML;
    fetch('/api/get_machine_code', {
        method : 'POST',
        body: JSON.stringify({
            id: id
        })
    })
    .then(response => response.json())
    .then(resp => {
        if (resp.result) {
            document.querySelector('#cuttingcode').hidden = false;
            document.querySelector('#breakpic').hidden = true;
            document.querySelector('#header-information').hidden = true;

            document.querySelector('#cuttingcode-value').innerHTML = resp.code;
        }
    }) 
}

/**
 * shows breakpic div
 * @returns early if display is already active
 */
function show_breakpic() {
    if (!document.querySelector('#breakpic').hidden){
        return;
    }

    document.querySelector('#cuttingcode').hidden = true;
    document.querySelector('#breakpic').hidden = false;
    document.querySelector('#header-information').hidden = true;
}

/**
 * retrieves header information via api and sets them to screen
 * @returns early if display is already active
 */
function show_header_information() {
    if (!document.querySelector('#header-information').hidden){
        return;
    }

    let id = document.querySelector('#pattern-id').innerHTML;
    fetch('/api/get_header_information', {
        method : 'POST',
        body: JSON.stringify({
            id: id
        })
    })
    .then(response => response.json())
    .then(resp => {
        if (resp.result) {
            document.querySelector('#cuttingcode').hidden = true;
            document.querySelector('#breakpic').hidden = true;
            document.querySelector('#header-information').hidden = false;

            let cont = document.querySelector('#header-information-content');
            cont.innerHTML = ""
            for (let [key, value] of Object.entries(resp.data)) {
                
            
                if (value.constructor == Object){
                    for (let [inner_key, inner_value] of Object.entries(value)){
                        var tmp = document.createElement("h5");
                        tmp.innerHTML = `${key}-${inner_key}: ${inner_value}`;
                        cont.appendChild(tmp);
                    }
                }
                else if (value) {
                    var tmp = document.createElement("h5");
                    tmp.innerHTML = `${key}: ${value}`;
                    cont.appendChild(tmp);
                }
            }
        }
    }) 
}

/**
 * sends a request to api, gets the machine code and saves it to client
 */
function down_load_edi_file(){
    let id = document.querySelector('#pattern-id').innerHTML;
    fetch('/api/get_machine_code', {
        method : 'POST',
        body: JSON.stringify({
            id: id
        })
    })
    .then(response => response.json())
    .then(resp => {
        if (resp.result) {
            var file = new Blob([resp.code], {type: "text/plain"});
            if (window.navigator.msSaveOrOpenBlob) // IE10+
            window.navigator.msSaveOrOpenBlob(file, filename);
            else { // Others
                var a = document.createElement("a"),
                        url = URL.createObjectURL(file);
                a.href = url;
                a.download = resp.name;
                document.body.appendChild(a);
                a.click();
                setTimeout(function() {
                    document.body.removeChild(a);
                    window.URL.revokeObjectURL(url);  
                }, 0); 
            }
        }
    })
}

/**
 * sets the visibilty for customers in the add cutting plan form
 */
function show_add_customer() {
    loadCustomerGroups();
    document.querySelector('#customer-text').hidden = false;
    document.querySelector('#select-customer').hidden = true;
    
    document.querySelector('#add-customer').hidden = true;
    document.querySelector('#hide-customer').hidden = false;
    
    document.querySelector('#add-customer-group').hidden = false;
    document.querySelector('#hide-customer-group').hidden = true;

    document.querySelector('#text-customer-group').hidden = true;
    document.querySelector('#select-customer-group').hidden = false;
}

/**
 * hides the customer text fields
 */
function hide_add_customer() {
    document.querySelector('#customer-text').hidden = true;
    document.querySelector('#select-customer').hidden = false;
    
    document.querySelector('#add-customer').hidden = false;
    document.querySelector('#hide-customer').hidden = true;
}

/**
 * shows the textfield for customer group
 */
function show_add_customer_group() {
    loadCustomerGroups();
    document.querySelector('#text-customer-group').hidden = false;
    document.querySelector('#select-customer-group').hidden = true;
    
    document.querySelector('#add-customer-group').hidden = true;
    document.querySelector('#hide-customer-group').hidden = false;
}

/**
 * hides the textfield for customer groups
 */
function hide_add_customer_group() {

    document.querySelector('#text-customer-group').hidden = true;
    document.querySelector('#select-customer-group').hidden = false;
    
    document.querySelector('#add-customer-group').hidden = false;
    document.querySelector('#hide-customer-group').hidden = true;

}

/**
 * redirects the user to the given cuttingpattern page
 * @param {number} location id of page to show
 */
function redirect(location){
    window.location.href = "./cuttingpattern/" + location;
}

//setting click events for cuttingplans and the delete icos
var arr = document.querySelector('#cp-display')?.children;
for (let idx = 0; idx <= arr?.length; idx++) {
    let element = arr[idx];
    if (!element) {
        continue;
    }

    element.addEventListener("click", function(e) {
        redirect(this.id);
    })

    var ico = element.querySelector('#delete-ico');
    ico?.addEventListener("click", function(e) {
        e.stopPropagation();
        send_delete(element.id);
    })    
}

/**
 * send api request to delete given cuttingpattern
 * @param {number} id id of cuttingpattern
 */
function send_delete(id) {
    fetch('/api/delete_pattern', {
        method : 'POST',
        body: JSON.stringify({
            id: id
        })
    })
    .then(response => response.json())
    .then(resp => {
        if (resp.result) {
            location.reload(); 
        }
    }) 
}

/**
 * shows the cuttingplans which are related to the customer
 * @param {number} id of customer box to drop out
 */
function dropout(id) {
    let customer_li = document.querySelector(`#customer_${id}`);
    let tmp = customer_li.querySelector('.dropout-down');
    if (tmp) { // we want to display
        tmp.classList.remove('dropout-down');
        tmp.classList.add('dropout-up');
        let cp_view = document.querySelector(`#cp_prev_${id}`);
        cp_view.classList.remove('hidden');
        customer_li.style = "margin-bottom: 0";
        customer_li.classList.remove('row-indication');
        customer_li.classList.add('row-selected');
    }
    else {
        tmp = customer_li.querySelector('.dropout-up');
        if (tmp) {
            tmp.classList.remove('dropout-up');
            tmp.classList.add('dropout-down');
            let cp_view = document.querySelector(`#cp_prev_${id}`);
            cp_view.classList.add('hidden');
            customer_li.style = "";
            customer_li.classList.add('row-indication');
            customer_li.classList.remove('row-selected');
        }
    }
}

// event handler for exiting the form display
document.querySelector('#form-background')?.addEventListener("click", function(e) {
    toggleVisibility(e);
});

/**
 * toggles visibility of from
 * @param {Event} e event obj
 * @returns if target is not the backgorund
 */
function toggleVisibility(e) {
    if(e.target !== e.currentTarget) return;

    let tmp = document.querySelector('#form-background');
    if (tmp && !tmp.hidden) {
        tmp.hidden = true
    }
    else if (tmp && tmp.hidden){
        tmp.hidden = false
    }
}

document.querySelector('#new-cp')?.addEventListener("submit", sendNewCuttingPlan);


/**
 * sends an api request to create a new cuttingpattern
 * @param {Event} e event obj
 */
function sendNewCuttingPlan(e) {
    e.preventDefault();

    let file_name = document.querySelector("#file_name").value;
    let description = document.querySelector("#description").value;
    let customer = "";
    let customer_group = "";
    //get correct entries from form, depending on visibility
    let sel = document.querySelector("#select-customer");
    if (!sel.hidden) {
        customer = sel.options[sel.selectedIndex].text;
    }
    else {
        let txt_c = document.querySelector("#text-customer");
        let txt_gc = document.querySelector("#text-customer-group");
        customer = txt_c.value;
        customer_group = txt_gc.value;
    }

    let file = document.querySelector("#machine_code").files[0];
    var machine_code = "";
    if (file) {
        var reader = new FileReader();
        reader.readAsText(file, "UTF-8");
        reader.onload = function (evt) {
            machine_code = evt.target.result;
            fetch('/api/add_cutting_pattern', {
                method : 'POST',
                body: JSON.stringify({
                    file_name: file_name,
                    description: description,
                    machine_code: machine_code,
                    customer : customer,
                    customer_group : customer_group
                })
            })
            .then(response => response.json())
            .then(resp => {
                if (resp.result) {
                    let tmp = document.querySelector('#form-background');
                    if (tmp && !tmp.hidden){
                        tmp.hidden = true;
                    } 
                    redirect(resp.id);
                }
            })
        }

        reader.onerror = function (evt) {
            alter("Error while reading file!");
        }
    }
}

/**
 * shows the form for adding a cuttingpattern
 */
function show_app_cp() {
    loadCustomers();
    let tmp = document.querySelector('#form-background');
    if (tmp && tmp.hidden){
        tmp.hidden = false
    }
}

/**
 * send an api request to get all customers and loads it to the select element
 */
function loadCustomers() {
    let selector = document.querySelector('#select-customer');
    if (selector) {
        selector.innerHTML = "";
    }

    fetch('/api/get_customers', {
        method : 'POST',
        body: ""
    })
    .then(response => response.json())
    .then(resp => {
        if (resp.result) {
            let sel = document.querySelector('#select-customer');
            let idx = 0;
            resp.customers.forEach(elem => {
                let opt = document.createElement('option');
                opt.value = idx++;
                opt.innerHTML = elem;
                sel.appendChild(opt);
            });
        }
    })
}

/**
 * sends an api request to get all customer groups an loads them to the select in form
 */
function loadCustomerGroups() {
    let selector = document.querySelector('#select-customer-group');
    if (selector) {
        selector.innerHTML = "";
    }

    fetch('/api/get_customer_groups', {
        method : 'POST',
        body: ""
    })
    .then(response => response.json())
    .then(resp => {
        if (resp.result) {
            let sel = document.querySelector('#select-customer-group');
            let idx = 0;
            resp.groups.forEach(elem => {
                let opt = document.createElement('option');
                opt.value = idx++;
                opt.innerHTML = elem;
                sel.appendChild(opt);
            });
        }
    })
}

//following to functions were copied from https://developer.mozilla.org/en-US/docs/Web/API/HTML_Drag_and_Drop_API/File_drag_and_drop
//some changes are applied to prefill the form

/**
 * Gets called on drop event
 * @param {Event} ev event object
 */
function dropHandler(ev) {
  
    // Prevent default behavior (Prevent file from being opened)
    ev.preventDefault();
  
    if (ev.dataTransfer.items) {
      // Use DataTransferItemList interface to access the file(s)
      for (var i = 0; i < ev.dataTransfer.items.length; i++) {
        // If dropped items aren't files, reject them
        if (ev.dataTransfer.items[i].kind === 'file') {
          var file = ev.dataTransfer.items[i].getAsFile();
          
          let file_input = document.querySelector('#machine_code');
          file_input.files = ev.dataTransfer.files;
          document.querySelector('#file_name').value = file.name
          show_app_cp()
        }
      }
    } else {
      // Use DataTransfer interface to access the file(s)
      for (var i = 0; i < ev.dataTransfer.files.length; i++) {
          let file_input = document.querySelector('#machine_code');
          file_input.files = ev.dataTransfer.files;
          document.querySelector('#file_name').value = file.name
          show_app_cp()

      }
    }
  }

/**
 * gets called by drag over handler
 * @param {Event} ev event object
 */
function dragOverHandler(ev) {  
    // Prevent default behavior (Prevent file from being opened)
    ev.preventDefault();
  }