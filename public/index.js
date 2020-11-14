//get the video element from the DOM
const videoElement = document.querySelector("video");
const videoSelect = document.querySelector("select#videoSource");

videoSelect.onchange = getStream;

//entry
streamVideo().catch(handleError);

async function streamVideo() {
    await getStream();
    let deviceInfos = await getDevices();
    await gotDevices(deviceInfos);
}

//checks that the browser supports getUserMedia()
async function hasGetUserMedia() {
    if (!!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia)) {
        //good to go
    } else {
        throw new Error("Browser does not support getUserMedia()");
    }
}

//gets available devices using enumerateDevices()
async function getDevices() {
    hasGetUserMedia();
    return navigator.mediaDevices.enumerateDevices();
}

//once we have the devices we can append them to the devices dropdown
async function gotDevices(deviceInfos) {
    window.deviceInfos = deviceInfos;
    console.log("Available input and output devices:", deviceInfos);
    for (let deviceInfo of deviceInfos) {
        const option = document.createElement("option");
        option.value = deviceInfo.deviceId;
        if (deviceInfo.kind === "videoinput") {
            option.text =
                deviceInfo.label || "camera " + (videoSelect.length + 1);
            videoSelect.appendChild(option);
        }
    }
}

//gets the users video stream using getUserMedia(), will prompt the user for access to their webcam
async function getStream() {
    if (window.stream) {
        window.stream.getTracks().forEach((track) => track.stop());
    }

    const videoSource = videoSelect.value;
    const hdConstraints = {
        video: true,
    };

    let stream = await navigator.mediaDevices.getUserMedia(hdConstraints);
    await gotStream(stream);
}

//sets the HTML5 video element to the stream from the users webcam
async function gotStream(stream) {
    window.stream = stream; //make stream available to the console
    videoSelect.selectedIndex = [...videoSelect.options].findIndex(
        (option) => option.text === stream.getVideoTracks()[0].label
    );
    videoElement.srcObject = stream;
}

async function handleError(error) {
    console.error("Error: ", error);
}
