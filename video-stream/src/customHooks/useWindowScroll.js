// COPIED AND PASTED FROM GOOGLE SEARCH AI
import { useState, useEffect } from "react";

function useWindowScroll() {
  const [scrollPosition, setScrollPosition] = useState({
    x: 0,
    y: 0,
  });

  useEffect(() => {
    function handleScroll() {
      setScrollPosition({
        x: window.scrollX,
        y: window.scrollY,
      });
    }

    window.addEventListener("scroll", handleScroll);

    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return scrollPosition;
}
