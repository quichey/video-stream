import React, { useState } from "react";
import PropTypes from "prop-types";
import zxcvbn from "zxcvbn";

export default function PasswordInput({ value, onChange, label = "Password" }) {
  const [error, setError] = useState("");
  const strength = zxcvbn(value || "");

  const handleChange = (e) => {
    const input = e.target.value;
    onChange(input);

    if (input.length < 8) {
      setError("Password must be at least 8 characters.");
    } else {
      setError("");
    }
  };

  const strengthColors = ["bg-red-500", "bg-orange-500", "bg-yellow-500", "bg-green-400", "bg-green-600"];
  const strengthLabels = ["Too Weak", "Weak", "Fair", "Good", "Strong"];

  return (
    <div className="flex flex-col gap-1 w-full">
      <label className="text-sm font-medium text-gray-700">{label}</label>
      <input
        type="password"
        value={value}
        onChange={handleChange}
        className={`p-2 border rounded-lg focus:outline-none focus:ring ${
          error ? "border-red-500" : "border-gray-300"
        }`}
        placeholder="Enter password"
      />
      {error && <p className="text-xs text-red-500">{error}</p>}

      {value && (
        <div className="mt-1">
          <div className="flex gap-1">
            {[0, 1, 2, 3, 4].map((i) => (
              <div
                key={i}
                className={`h-2 flex-1 rounded ${
                  i <= strength.score ? strengthColors[strength.score] : "bg-gray-200"
                }`}
              />
            ))}
          </div>
          <p className="text-xs text-gray-600 mt-1">{strengthLabels[strength.score]}</p>
        </div>
      )}
    </div>
  );
}

PasswordInput.propTypes = {
  value: PropTypes.string.isRequired,
  onChange: PropTypes.func.isRequired,
  label: PropTypes.string,
};
