// COPIED AND PASTED FROM GOOGLE SEARCH AI
import { useState, useEffect } from "react";

export default function useWindowScroll() {
  const [scrollPosition, setScrollPosition] = useState({
    x: 0,
    y: 0,
  });

  useEffect(() => {
    function handleScroll() {
      setScrollPosition(() => {
        const x = window.scrollX;
        const y = window.scrollY;
        const maxY =
          document.documentElement.scrollHeight -
          document.documentElement.clientHeight;
        const yPercent = (y / maxY) * 100;
        return {
          x,
          y,
          maxY,
          yPercent,
        };
      });
    }

    window.addEventListener("scroll", handleScroll);

    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return scrollPosition;
}
