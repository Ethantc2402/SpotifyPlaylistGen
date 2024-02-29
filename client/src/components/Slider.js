import { useState } from "react";
import "../css/slider.css";

const Slider = ({ type, range, interval }) => {
  const [value, setValue] = useState(range[0]);

  const updateValue = (e) => {
    setValue(e.target.value);
  };

  return (
    <div className="slidecontainer">
      <input
        id={type === "Mood/Valence" ? "mood_valence" : type.toLowerCase()}
        className="slider"
        type="range"
        step={interval}
        min={range[0]}
        max={range[1]}
        defaultValue={range[0]}
        onChange={updateValue}
      />
      <div className="type">{type}</div>
      <div>{value}</div>
    </div>
  );
};

export default Slider;
