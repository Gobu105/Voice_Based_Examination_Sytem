function speak(text) {
    const msg = new SpeechSynthesisUtterance(text);
    window.speechSynthesis.speak(msg);
}

function startExam() {
    speak("The exam has started. Please listen carefully.");
}