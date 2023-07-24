/*! 
  BreakPicture alias BP
*/
var xmlns = "http://www.w3.org/2000/svg";

/**
 * Sends an API request to get the cutting pattern from the given id
 * @param {number} id Id of cutting pattern to retrieve
 */
function getCuttingPattern(id) {
    fetch('/api/get_cutting_pattern', {
        method : 'POST',
        body: JSON.stringify({
            id: id
        })
    })
    .then(response => response.json())
	.then(resp => {
        if (resp.result) {
            InitCuttingPlan(0, resp.file ,document.getElementById('Parent'), false)
        }
    })
}

/**
 * This is just a simple wrapper class for the Header information
 */
class Header{
	/**
	 * sets given header information
	 * @param {JSON} json Header part of received json
	 */
	constructor(json) {
		this.Header = json
	}
}
/**
 * This is just a simple wrapper class for the Body information
 */
class Body{
	/**
	 * set given Body information
	 * @param {JSON} json Body part of received json
	 */
	constructor(json){
		this.Body = json
	}
}

/**
 * global data variable for header information
 */
let _Header;

/**
 * global data variable for body information
 */
let _Body;

/**
 * global variable for saving previous selected element
 */
let PreviousElement;

/**
 * global variable for storing factor for drawing
 */
let factorBreakPic = 0;

/**
 * Checks if the JSON Object is empty
 * @param {JSON} obj object to be checked
 * @returns true if empty, false if not
 */
function isEmpty(obj) {
    for(var prop in obj) {
        if(obj.hasOwnProperty(prop))
            return false;
    }
    return true;
}

/**
 * This function renders the given sheets, with all its childs to the given parent
 * @param {JSON} sheet json object to be drawn
 * @param {HTMLElement} parent element to be drawn on
 * @param {number} r_point [0,1,2,3] relation point of cuttingplan
 */
function DrawSheet(sheet, parent, r_point) {
	let Trav = document.createElement("div");
	let dir_name = "", cut_edge = `${sheet.CutType}Travere`;
	if (sheet.CutType == "X" || sheet.CutType == "Z" || sheet.CutType == "W") {
		//set direction class
		if (r_point == 0 || r_point == 1) {
			dir_name = "U";
			if (r_point == 0) {
				cut_edge += "L";
			}
			else if (r_point == 1) {
				cut_edge += "R"
			}
		}
		else {
			dir_name = "O";
			if (r_point == 0 || r_point == 1) {
				cut_edge += "L";
			}
			else {
				cut_edge += "R"
			}
		}
		Trav.setAttribute("style", "width: " + sheet.Width * factorBreakPic + "px;");
	}
	else if (sheet.CutType == "Y" || sheet.CutType == "V") {
		//set direction class
		if (r_point == 0 || r_point == 2) {
			dir_name = "R";
			if (r_point == 0) {
				cut_edge += "O";
			}
			else if (r_point == 2) {
				cut_edge += "U"
			}
		}
		else {
			dir_name = "L";
			if (r_point == 1) {
				cut_edge += "O";
			}
			else if (r_point == 3) {
				cut_edge += "U"
			}
		}
		Trav.setAttribute("style", "height: " + sheet.Height * factorBreakPic + "px;");
	}
	Trav.className = dir_name;
	Trav.classList.add(cut_edge);
	if (!isEmpty(sheet.TraverseInformation) || !sheet.Childs.length) {
		Trav.setAttribute("id", sheet.TraverseInformation.TravId);
		Trav.addEventListener("click", function() {
			getSheetInfo(this, sheet);
		})
		Trav.addEventListener("contextmenu", function(e){
			e.preventDefault()
			let source = e.target || e.srcElement;
			if (source.nodeName != "DIV"){
				source = source.parentElement
			}
			console.log(sheet)
		})
	}

	if (!sheet.RackCode && !sheet.Childs.length) {
		sheet.RackCode = "B0";
	}
	
	if (sheet.RackCode || !sheet.Childs.length) {
		setNameTag(Trav, sheet)
	}

	parent.appendChild(Trav);
	for (let idx = 0; idx < sheet.Childs.length; idx++) {
		DrawSheet(sheet.Childs[idx], Trav, r_point);
	}
}

/**
 * THis function creats the name tag for each sheet, also sets the sheet class
 * @param {HTMLElement} element parent element to be drawn on
 * @param {JSON} sheet json object of sheet
 */
function setNameTag(element, sheet) {
	var txtNode = document.createTextNode(
		(sheet.RackCode + " \n " + sheet.Width + " x " + sheet.Height)
	);

    var textField = document.createElement("p");
    textField.classList.add("isCenterTextBP");
    textField.appendChild(txtNode);
    textField.setAttribute("style", "font-size:"+ ((100*factorBreakPic) - 1) +"px;");

    element.appendChild(textField);

    element.classList.add("isSheet");
}

/**
 * Renders the cutting plan to given parent
 * @param {number} direction Indication for Zero point of cutting pattern
 * @param {JSON} json Sheet information
 * @param {HTMLDivElement} parent Parent to draw the cutting pattern on
 * @returns if successfull or not
 */
function InitCuttingPlan(direction, json, parent) {
	//check for parent obj
	let CP  = document.querySelector("#CuttingPlan")
	if (CP == null) {
		CP = document.createElement("div");
		CP.setAttribute("id","CuttingPlan");
	}

	//for future feature - TODO: add new context menue to add cuts
	CP.addEventListener("contextmenu", function(e) {
		e.preventDefault();

		let source = e.target || e.srcElement;
		if (source.nodeName != "DIV"){
			source = source.parentElement
		}

	})
    
    var json_buff = JSON.parse(json)
	_Header = new Header(json_buff["Header"])
	_Body = new Body(json_buff["Body"])

    if(parent) {
		parent.appendChild(CP);
    }
    else {
		console.log("No Parent!");
		return false;
    }
    
	//set parents relation point
    switch(direction)  {
		case 0:
			CP.className = "R";
		break;
		case 1:
			CP.className = "L";
		break;
		case 2:
			CP.className = "R";
		break;
		case 3:
			CP.className = "L";
		break;
		default:
			console.log("FAILURE IN DIRECTIONSETTINGS");
    }
    
    CP.innerHTML = "";
	
    var jqParent = $(parent);
    
    let parentHeight = jqParent.innerHeight();
    let parentWidth = jqParent.innerWidth();

    let scaleX = parentWidth / _Body.Body.Width;
    let scaleY = parentHeight / _Body.Body.Height;
    factorBreakPic = scaleX < scaleY?scaleX:scaleY;
    
    //Set Attributes
    CP.setAttribute("style" ,"height: "+ _Body.Body.Height * factorBreakPic + "px;");
    CP.setAttribute("style" ,"width: "+ _Body.Body.Width * factorBreakPic + "px;");

	for (let idx = 0; idx < _Body.Body.Childs.length; idx++) {
		DrawSheet(_Body.Body.Childs[idx], CP, 0);
	}

	// right after drawing check the sheet text if it fits to the parent
	CheckLabelsForFitting(CP);
	
	// first add general Information
	addGeneralInformation();
}

/**
 * Checks all child labels width the class isCenterTextBP and hides them if they are overflowing
 * @param {HTMLElement} element Element to check labels for
 */
function CheckLabelsForFitting(element) {
	let buff = element.querySelector('.isCenterTextBP')
	if (element.classList.contains("isSheet") &&  buff) {		
		if (isOverflown(element)){
			 buff.classList.add("hide");
		 }
	}
	for (let idx = 0; idx < element.children.length; idx++) {
		CheckLabelsForFitting(element.children[idx]);
	}
}

/**
 * Check if the given element has overflowing childs
 * @param {HTMLElement} element Element to be checked for overflowing
 * @returns true if element has overflow
 */
function isOverflown(element){
	return element.scrollHeight > element.clientHeight || element.scrollWidth > element.clientWidth;
  }

/**
 * Set the information of clicked sheet to info screen
 * @param {HTMLElement} element elem which has been clicked
 * @param {JSONObject} sheet json object with sheet infos
 */
function getSheetInfo(element, sheet)
{
    if(PreviousElement)  {
		PreviousElement.classList.remove("selected");
		element.classList.add("selected");
		PreviousElement = element; 
    }
    else {
		element.classList.add("selected");
		PreviousElement = element; 
    }

	let elem = document.querySelector('#sheet-info');
	//first clear
	elem.innerHTML = "";
	elem.hidden = false;

	if (sheet.RackCode) {
		var desc = document.createElement("h4");
		desc.innerHTML = sheet.RackCode;
		elem.appendChild(desc);
	}
	else {
		var desc = document.createElement("h4");
		desc.innerHTML = "No Rack information given!";
		elem.appendChild(desc);	
	}

	var leaf_size = document.createElement("h4");
	leaf_size.innerHTML = sheet.Width + " x " + sheet.Height;
	elem.appendChild(leaf_size);

	for (let [key, value] of Object.entries(sheet.TraverseInformation)) {
		var tmp = document.createElement("h5");
		if (value) {
			tmp.innerHTML = `${key}: ${value}`;
		}
		else {
			tmp.innerHTML = `${key}`;
		}
		elem.appendChild(tmp);
	  }
}

/**
 * Sets the genral information to an info field
 * @returns can be returning early if the info filed is not present
 */
function addGeneralInformation() {
	let info_cont = document.querySelector('#info');
	if (!info_cont) {
		return;
	}

	//setting parents sheet size
	let size_label = document.createElement("h4");
	size_label.innerHTML = _Header.Header["Widht"] + "mm x " + _Header.Header["Height"] + "mm";
	info_cont.appendChild(size_label);

	//calculate used area of child cuts
	var avail = _Header.Header["Widht"] * _Header.Header["Height"];
	var used = 0;
	for (let idx = 0; idx < _Body.Body.Childs.length; idx++) {
		used += getUsedArea(_Body.Body.Childs[idx]);
	}
	let usage = document.createElement("h4");
	
	usage.innerHTML = "Usage: " + (used / (avail/100)).toPrecision(4) + "%";
	info_cont.appendChild(usage);
}

/**
 * Calculates the used area of the given leaf recursively
 * @param {JSONObject} leaf json object of leaf
 * @returns used area of all childs
 */
function getUsedArea(leaf) {
	let result = 0.0;
	if ((leaf.RackCode || !leaf.Childs.length) && (leaf.RackCode != "B99" && leaf.RackCode != "B98")) {
		result = leaf.Height * leaf.Width;
	}

	for (let idx = 0; idx < leaf.Childs.length; idx++) {
		result += getUsedArea(leaf.Childs[idx]);
	}
	return result
}


/**
 * Adds the model information to the div
 * @param {String} data Model information
 * @param {HTMLDivElement} element Parent elemt to draw model on 
 */
function addModel(data, element)
{
    var arcArray;
    var gotArcs = false;
    if(data.includes("R"))
    {
		arcArray = data.match(/(R)[0-9,\., ]*(X)[0-9,\., ]*(Y)[0-9,\., ]*(x)[0-9,\., ]*(y)[0-9,\., ]*/gi);
		data = data.replace(/(R)[0-9,\., ]*(X)[0-9,\., ]*(Y)[0-9,\., ]*(x)[0-9,\., ]*(y)[0-9,\., ]*/gi,'Arc ');
		data = data.replace(/[x,y]/g,'');
		data = data.replace(/(X)([0-9,.]*)/g,'');
		data = data.replace(/(Y)([0-9,.]*)/g,'');
		data = data.replace(/( * )/g,' ');
    }
    else
    {
		data = data.replace(/(R)[0-9,\., ]*(X)[0-9,\., ]*(Y)[0-9,\., ]*(x)[0-9,\., ]*(y)[0-9,\., ]*/gi,'Arc ');
		data = data.replace(/[X,Y]/g,'');
		data = data.replace(/(y)([0-9,.]*)/g,'');
		data = data.replace(/(x)([0-9,.]*)/g,'');
		data = data.replace(/( * )/g,' ');	
    }
    
    var dataarray = data.split(' ');
    var pString = "";

    pString = "";
    var arcsCounter = 0;

    console.log(arcArray);
    console.log(dataarray);

    for(var i = 0; i < dataarray.length; i++)   {
		if(dataarray[i] != "")	{

	    	if(dataarray[i] != "Arc" && pString == "")   {
				pString += "M" + dataarray[i++]*factorBreakPic + " ";
				pString += dataarray[i]*factorBreakPic + " ";
	    	}
	    	else {
				if( dataarray[i] != "Arc" ) {
					pString += "L" + dataarray[i]*factorBreakPic + " ";
					i++;
					pString += dataarray[i]*factorBreakPic + " ";
				}
				else {
					var tempArray = arcArray[arcsCounter].split(' ');
					console.log(tempArray);

					var start = polarToCartesian(tempArray[1].replace(/[A-Z,a-z]*/g,'')*factorBreakPic,
								tempArray[2].replace(/[A-Z,a-z]*/g,'')*factorBreakPic,
								tempArray[0].replace(/[A-Z,a-z]*/g,'')*factorBreakPic,
								tempArray[3].replace(/[A-Z,a-z]*/g,''));

					var end   = polarToCartesian(tempArray[1].replace(/[A-Z,a-z]*/g,'')*factorBreakPic,
								tempArray[2].replace(/[A-Z,a-z]*/g,'')*factorBreakPic,
								tempArray[0].replace(/[A-Z,a-z]*/g,'')*factorBreakPic,
								tempArray[4].replace(/[A-Z,a-z]*/g,''));
		    
					if(pString == "")
					{
						pString += "M" + start.x + " ";
						pString += start.y + " ";
					}
					
					pString += describeArc(
								start,
								end,
								tempArray[0].replace(/[A-Z,a-z]*/g,'')*factorBreakPic,
								tempArray[3].replace(/[A-Z,a-z]*/g,''),
								tempArray[4].replace(/[A-Z,a-z]*/g,'')
							);
					arcsCounter++;
					dataarray[i] = "done";
				}
	    	}
		}	
    }
    pString += " Z";

    
    var path = document.createElementNS(xmlns,"path");
    path.setAttributeNS(null,'d', pString);
    path.setAttributeNS(null,'style', "height:" + (element.style.height?element.style.height:"100%") + "; width:" + (element.style.width?element.style.width:"100%") + ";");
    
    var svg = document.createElementNS(xmlns,'svg');
    svg.classList.add('ModelPath');
    svg.setAttributeNS(null,'style', "height:" + (element.style.height?element.style.height:"100%") + "; width:" + (element.style.width?element.style.width:"100%") + ";");
    svg.appendChild(path);
    element.appendChild(svg);
}

/**
 * Converts Polar cordinates into cartesian
 * @param {number} centerX 
 * @param {number} centerY 
 * @param {number} radius 
 * @param {number} angleInDegrees 
 * @returns Cartesian cordinates as JSON Obj
 */
function polarToCartesian(centerX, centerY, radius, angleInDegrees) {
  var angleInRadians = (angleInDegrees) * Math.PI / 180.0;

  return {
		x: centerX + (radius * Math.cos(angleInRadians)),
		y: centerY + (radius * Math.sin(angleInRadians))
 	 };
}

/**
 * 
 * @param {number} start 
 * @param {number} end 
 * @param {number} radius 
 * @param {number} startAngle 
 * @param {number} endAngle 
 * @returns String for arc model
 */
function describeArc(start, end, radius, startAngle, endAngle){
    
//  var largeArcFlag = endAngle - startAngle <= 180 ? "0" : "1";

    var d = [
        "A", radius, radius, 0, 0, 0, end.x, end.y
    ].join(" ");
    d += " ";

    return d;       
}