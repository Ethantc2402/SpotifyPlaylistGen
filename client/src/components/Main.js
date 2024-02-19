import Slider from "../components/Slider";
import "../css/main.css";

const sendFeatures = (features) => {
  fetch(`http://localhost:8080/post_features`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(features),
  })
    .then((res) => res.json())
    .then((features) => console.log(features))
    .catch((err) => console.log(err));
};

const Main = () => {
  const submitForm = (e) => {
    e.preventDefault();
    const sliderData = {};

    for (const slider of e.target.elements) {
      if (slider.type === "range") {
        sliderData[slider.id] = slider.value;
      }
    }

    sendFeatures(sliderData);
    console.log(sliderData);
  };

  return (
    <div className='main'>
      <div className="container">
        <h1>Spotify Playlist Generator</h1>
        <h1 id="welcome">Welcome, [name]</h1>
        <h2>Start creating your personalized playlist with any prompt!</h2>
        <input id="prompt" placeholder="Enter your text here..." rows="4" cols="50" />
        <p>(Optional)  Fine Tune Your Playlist</p>
      </div>
      <form onSubmit={submitForm}>
        <div id="slider-container">
          <Slider type="Acousicness" range={[0, 1]} interval={"0.05"} />
          <Slider type="Instrumentalness" range={[0, 1]} interval={"0.05"} />
          <Slider type="Tempo" range={[60, 180]} interval={"1"} />
          <Slider type="Danceability" range={[0, 1]} interval={"0.05"} />
          <Slider type="Energy" range={[0, 1]} interval={"0.05"} />
          <Slider type="Mood/Valence" range={[0, 1]} interval={"0.05"} />
        </div>
        <button type="submit">Generate Playlist</button>
      </form>
    </div>
  );
};

export default Main;
