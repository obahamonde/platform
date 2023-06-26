export const useSynthesis = () => {
  const voice = ref<SpeechSynthesisVoice>(
    undefined as unknown as SpeechSynthesisVoice
  );
  const text = ref("");
  const speech = useSpeechSynthesis(text, { voice });

  const voices = ref<string[]>([]);

  const pickVoice = (voiceName: string) => {
    voice.value = window.speechSynthesis
      .getVoices()
      .find((voice) => voice.name === voiceName)!;
  };

  onMounted(() => {
    if (speech.isSupported.value) {
      // load at last
      setTimeout(() => {
        voices.value = window.speechSynthesis
          .getVoices()
          .map((voice) => voice.name);
        pickVoice("Google US English");
      }, 1000);
    }
  });

  const play = () => {
    if (!speech.isSupported.value) return;
    if (speech.status.value === "pause") {
      window.speechSynthesis.resume();
    } else {
      speech.speak();
    }
  };

  const pause = () => {
    if (!speech.isSupported.value) return;
    window.speechSynthesis.pause();
  };

  const stop = () => {
    if (!speech.isSupported.value) return;
    window.speechSynthesis.cancel();
  };

  return {
    text,
    voice,
    voices,
    pickVoice,
    pause,
    stop,
    play,
  };
};
