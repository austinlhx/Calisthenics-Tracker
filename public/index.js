//get the video element from the DOM
const videoElement = document.querySelector("#streamed");
const recordedElement = document.querySelector("#recorded");
const videoSelect = document.querySelector("select#videoSource");

const recordingStatusElement = document.querySelector("#recording-status");

videoSelect.onchange = getStream;

//setup a media stream from our webcam using WebRTC

//hide the recorded element initially
recordedElement.style.display = "none";

var recordedChunks;
var recordedVideoURL;
var mediaRecorder;

async function initVideo() {
    await streamVideo();
    let stream = videoElement.captureStream();
    mediaRecorder = new MediaRecorder(stream, { mimeType: "video/webm" });
    mediaRecorder.ondataavailable = handleDataAvailable;

    document.addEventListener("keypress", handleRecordVideo);
    // recordButton.addEventListener("click", () => recordVideo(mediaRecorder));
    // stopButton.addEventListener("click", () => stopRecording(mediaRecorder));
    // uploadButton.addEventListener("click", () => uploadVideo());
}

function handleRecordVideo() {
    document.removeEventListener("keypress", handleRecordVideo);

    recordVideo();

    document.addEventListener("keypress", handleStopRecording);
}
function handleStopRecording() {
    document.removeEventListener("keypress", handleStopRecording);

    stopRecording();

    document.addEventListener("keypress", handleRecordVideo);
}



async function recordVideo() {
    recordedChunks = [];
    mediaRecorder.start();

    recordedElement.style.display = "none";
    videoElement.style.display = "";

    recordingStatusElement.innerHTML =
        "Recording... Press any key to stop recording";

    console.log("Started recording video");
}

async function stopRecording() {
    mediaRecorder.stop();

    videoElement.style.display = "none";
    recordedElement.style.display = "";

    recordingStatusElement.innerHTML =
        "Video ready. Press any key to retry recording";

    
    console.log("Stopped recording video");
}

async function uploadVideo() {
    alert(recordedVideoURL);

    let a = document.createElement("a");
    document.body.appendChild(a);
    a.style = "display: none";
    a.href = recordedVideoURL;
    a.download = "test.webm";
    a.click();
    window.URL.revokeObjectURL(recordedVideoURL);
}

function setRecordedVideo() {
    let buffer = new Blob(recordedChunks);

    //set the recorded video element to have the recorded video
    
    recordedElement.src = window.URL.createObjectURL(buffer);

    let videoBuffer = new Blob(recordedChunks, { type: "video/webm" });

    recordedVideoURL = URL.createObjectURL(videoBuffer);
}

function dataURItoBlob(dataURI) {
    // convert base64 to raw binary data held in a string
    var byteString = atob(dataURI.split(",")[1]);

    // separate out the mime component
    var mimeString = dataURI.split(",")[0].split(":")[1].split(";")[0];

    // write the bytes of the string to an ArrayBuffer
    var arrayBuffer = new ArrayBuffer(byteString.length);
    var _ia = new Uint8Array(arrayBuffer);
    for (var i = 0; i < byteString.length; i++) {
        _ia[i] = byteString.charCodeAt(i);
    }

    var dataView = new DataView(arrayBuffer);
    var blob = new Blob([dataView], { type: mimeString });
    return blob;
}

function handleDataAvailable(event) {
    console.log("Data Available: ");
    if (event.data.size > 0) {
        recordedChunks.push(event.data);

        setRecordedVideo();
    } else {
        //
    }
}

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
    //window.deviceInfos = deviceInfos;
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
    // if (window.stream) {
    //     window.stream.getTracks().forEach((track) => track.stop());
    // }

    const videoSource = videoSelect.value;
    const hdConstraints = {
        video: {
            width: { min: 1024, ideal: 1280, max: 1920 },
            height: { min: 576, ideal: 720, max: 1080 },
        },
    };

    let stream = await navigator.mediaDevices.getUserMedia(hdConstraints);
    await gotStream(stream);
}

//sets the HTML5 video element to the stream from the users webcam
async function gotStream(stream) {
    //window.stream = stream; //make stream available to the console
    videoSelect.selectedIndex = [...videoSelect.options].findIndex(
        (option) => option.text === stream.getVideoTracks()[0].label
    );
    videoElement.srcObject = stream;
}

async function handleError(error) {
    console.error("Error: ", error);
}
