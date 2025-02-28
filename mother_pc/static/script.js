var socket = io.connect("http://" + document.domain + ":" + location.port);

socket.on("update_clients", function(data) {
    let pcSelect = document.getElementById("pc-select");
    pcSelect.innerHTML = "";
    data.clients.forEach(client => {
        let option = document.createElement("option");
        option.value = client;
        option.textContent = client;
        pcSelect.appendChild(option);
    });
});

socket.on("response", function(data) {
    let log = document.getElementById("log");
    let message = document.createElement("p");
    message.textContent = data.message;
    log.appendChild(message);
});

function sendCommand(command) {
    let pcSelect = document.getElementById("pc-select");
    let selectedPC = pcSelect.value;
    if (!selectedPC) {
        alert("No PC selected");
        return;
    }
    socket.emit("send_command", { pc: selectedPC, command: command });
}
