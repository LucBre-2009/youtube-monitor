async function findID(){


    const input = document
    .getElementById("input")
    .value
    .trim();


    const result = document
    .getElementById("result");


    const error = document
    .getElementById("error");


    result.classList.add("hidden");

    error.textContent = "";


    if(input === ""){

        error.textContent =
        "Bitte eine URL oder einen @Handle eingeben.";

        return;

    }


    let url = input;


    if(input.startsWith("@")){

        url =
        "https://www.youtube.com/" + input;

    }


    try{

        const response =
        await fetch(

        "https://api.allorigins.win/raw?url="
        + encodeURIComponent(url)

        );


        const html =
        await response.text();


        const match =
        html.match(
        /"channelId":"(UC[^"]+)"/
        );


        if(!match){

            error.textContent =
            "Keine Channel-ID gefunden.";

            return;

        }


        const id = match[1];


        document
        .getElementById("channelID")
        .textContent = id;


        result.classList.remove("hidden");


    }catch{

        error.textContent =
        "Fehler beim Abrufen der Daten.";

    }

}


function copyID(){

    const id = document
    .getElementById("channelID")
    .textContent;


    navigator.clipboard.writeText(id);

}