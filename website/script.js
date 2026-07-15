async function findChannel() {

    const input = document
        .getElementById("channelInput")
        .value
        .trim();


    const result = document
        .getElementById("result");

    const error = document
        .getElementById("error");


    result.classList.add("hidden");
    error.textContent = "";


    if (!input) {
        error.textContent =
            "Bitte eine URL eingeben.";
        return;
    }


    let url = input;


    if (input.startsWith("@")) {
        url =
        "https://www.youtube.com/" + input;
    }


    try {

        const response = await fetch(
            "https://api.allorigins.win/raw?url="
            + encodeURIComponent(url)
        );


        const html = await response.text();


        const match = html.match(
            /"channelId":"(UC[^"]+)"/
        );


        if (!match) {

            error.textContent =
            "Keine Channel-ID gefunden.";

            return;
        }


        const channelId = match[1];


        let nameMatch = html.match(
            /<title>(.*?) - YouTube<\/title>/
        );


        let name =
            nameMatch
            ? nameMatch[1]
            : "Unbekannt";


        document
        .getElementById("channelName")
        .textContent = name;


        document
        .getElementById("channelId")
        .textContent = channelId;


        result.classList.remove("hidden");


    } catch (e) {

        error.textContent =
        "Fehler beim Abrufen der Daten.";

    }
}



function copyId() {

    const id =
    document
    .getElementById("channelId")
    .textContent;


    navigator.clipboard.writeText(id);

}
