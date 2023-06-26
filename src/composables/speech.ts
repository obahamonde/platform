export const useSpeech = () => {
  const speech = useSpeechRecognition({
    continuous: true,
  });
  const SpeechGrammarList =
    window.SpeechGrammarList || window.webkitSpeechGrammarList;
  const speechRecognitionList = new SpeechGrammarList();
  speechRecognitionList.addFromString(1);
  speech.recognition!.grammars = speechRecognitionList;
  const { isListening, result } = speech;

  return {
    isListening,
    result,
    speech,
  };
};
