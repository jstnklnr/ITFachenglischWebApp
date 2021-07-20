window.addEventListener("load", () => {
    let switches = document.getElementsByClassName("selection-switch");

    for(let i = 0; i < switches.length; i++) {
        switches[i].parentElement.addEventListener("click", () => {
            let checkbox = switches[i].getElementsByTagName("input")[0];
            checkbox.checked = !checkbox.checked;
        });
    }

    let ranges = document.getElementsByClassName("range-selection");

    for(let i = 0; i < ranges.length; i++) {
        let range = ranges[i].getElementsByTagName("input")[0]

        let label = ranges[i].getElementsByTagName("label")[0];
        label.innerText = `${label.dataset.text}: ${range.value}`;

        range.addEventListener("change", () => {
            label.innerText = `${label.dataset.text}: ${range.value}`;
        });
    }

    let constructions = document.getElementsByClassName("text-construction");
    let addSelections = (construction, lowerSelectionList, upperSelectionList) => {
        construction.appendChild(document.createElement("hr"));

        for(let i = 0; i < upperSelectionList.length; i++) {
            let node = document.createElement("button");
            node.className = "border border-2 border-secondary rounded lead px-2 mt-1 mx-1 shadow upper-selection";
            node.innerText = upperSelectionList[i];
            node.addEventListener("click", evt => {
                lowerSelectionEvent(evt, construction, true);
            });

            construction.appendChild(node);
        }

        construction.appendChild(document.createElement("hr"));

        for(let i = 0; i < lowerSelectionList.length; i++) {
            let node = document.createElement("button");
            node.className = "border border-2 border-secondary rounded lead px-2 mt-1 mx-1 shadow lower-selection";
            node.innerText = lowerSelectionList[i];
            node.addEventListener("click", evt => {
                lowerSelectionEvent(evt, construction);
            });

            construction.appendChild(node);
        }
    }

    let lowerSelectionEvent = (event, construction, swap = false) => {
        let leadText = construction.getElementsByTagName("p")[0].innerText;

        let lowerSelectionList = [];
        let upperSelectionList = [];

        let lowerSelections = construction.getElementsByClassName(swap ? "upper-selection" : "lower-selection");
        let upperSelections = construction.getElementsByClassName(swap ? "lower-selection" : "upper-selection");
        
        let selectedText = event.target.innerText;
        
        for(let i = 0; i < lowerSelections.length; i++) {
            if(lowerSelections[i] != event.target)
                lowerSelectionList.push(lowerSelections[i].innerText);
        }

        if(lowerSelections.length > 0)
            for(let i = lowerSelections.length - 1; i >= 0; i--) {
                lowerSelections[i].remove();
            }

        /**/

        for(let i = 0; i < upperSelections.length; i++) {
            upperSelectionList.push(upperSelections[i].innerText);
        }

        upperSelectionList.push(selectedText);

        if(upperSelections.length > 0)
            for(let i = upperSelections.length - 1; i >= 0; i--) {
                upperSelections[i].remove();
            }

        construction.innerHTML = "";

        let newLead = document.createElement("p");
        newLead.className = "display-6";
        newLead.innerText = leadText;

        construction.appendChild(newLead);
        addSelections(construction, swap ? upperSelectionList : lowerSelectionList, swap ? lowerSelectionList : upperSelectionList);
    };

    for(let i = 0; i < constructions.length; i++) {
        let lead = constructions[i].getElementsByTagName("p")[0];
        let lowerSelectionList = lead.dataset.words.split(" ");

        addSelections(constructions[i], lowerSelectionList, []);
    }
});