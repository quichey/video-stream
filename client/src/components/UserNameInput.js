import React, { useState } from "react";
import PropTypes from "prop-types";
import * as leoProfanity from "leo-profanity"; // for profanity filter

// Allowed username: 3-20 chars, alphanumeric + . _
const USERNAME_REGEX = /^[a-zA-Z0-9._]{3,20}$/;

export default function UserNameInput({ value, onChange, label = "Username" }) {
  const [error, setError] = useState("");

  const handleChange = (e) => {
    const input = e.target.value;
    onChange(input);

    if (!USERNAME_REGEX.test(input)) {
      setError("3–20 characters, letters/numbers/._ only.");
    } else if (leoProfanity.check(input)) {
      setError("Username contains inappropriate words.");
    } else {
      setError("");
    }
  };

  return (
    <div className="flex flex-col gap-1 w-full">
      <label className="text-sm font-medium text-gray-700">{label}</label>
      <input
        type="text"
        value={value}
        onChange={handleChange}
        className={`p-2 border rounded-lg focus:outline-none focus:ring ${
          error ? "border-red-500" : "border-gray-300"
        }`}
        placeholder="Enter username"
      />
      {error && <p className="text-xs text-red-500">{error}</p>}
    </div>
  );
}

UserNameInput.propTypes = {
  value: PropTypes.string.isRequired,
  onChange: PropTypes.func.isRequired,
  label: PropTypes.string,
};
