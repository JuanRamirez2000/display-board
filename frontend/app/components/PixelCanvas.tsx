"use client";

import { useState, useCallback } from "react";
import { HexColorPicker } from "react-colorful";

const GRID_SIZE = 32;
const TOTAL_PIXELS = GRID_SIZE * GRID_SIZE; // 1024

// Convert hex color (#ff0000) to [R, G, B]
function hexToRgb(hex: string): [number, number, number] {
  const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  return result
    ? [
        parseInt(result[1], 16),
        parseInt(result[2], 16),
        parseInt(result[3], 16),
      ]
    : [0, 0, 0];
}

export default function PixelCanvas() {
  const [grid, setGrid] = useState<string[]>(
    Array(TOTAL_PIXELS).fill("#ffffff"),
  );
  const [color, setColor] = useState("#ff0000");
  const [tool, setTool] = useState<"paint" | "erase">("paint");
  const [isPainting, setIsPainting] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [showPicker, setShowPicker] = useState(false);

  const paintCell = useCallback(
    (index: number) => {
      setGrid((prev) => {
        const next = [...prev];
        next[index] = tool === "erase" ? "#ffffff" : color;
        return next;
      });
    },
    [tool, color],
  );

  const handleSubmit = async () => {
    const pixels = grid.map((hex) => hexToRgb(hex));
    await fetch("http://localhost:8000/api/submit", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ pixels }),
    });
    setSubmitted(true);
    setTimeout(() => setSubmitted(false), 2000);
  };

  return (
    <div className="flex flex-col items-center gap-6 p-8">
      <h1 className="text-2xl font-bold">Pixel Pi 🎨</h1>

      {/* Toolbar */}
      <div className="flex gap-3 items-center">
        <button
          onClick={() => setTool("paint")}
          className={`px-4 py-2 rounded font-medium ${
            tool === "paint" ? "bg-blue-500 text-white" : "bg-gray-200"
          }`}
        >
          Paint
        </button>
        <button
          onClick={() => setTool("erase")}
          className={`px-4 py-2 rounded font-medium ${
            tool === "erase" ? "bg-blue-500 text-white" : "bg-gray-200"
          }`}
        >
          Erase
        </button>

        {/* Color swatch — click to toggle picker */}
        <div className="relative">
          <div
            onClick={() => setShowPicker((p) => !p)}
            className="w-10 h-10 rounded border-2 border-gray-400 cursor-pointer"
            style={{ backgroundColor: color }}
          />
          {showPicker && (
            <div className="absolute top-12 left-0 z-10">
              <HexColorPicker color={color} onChange={setColor} />
            </div>
          )}
        </div>

        <button
          onClick={() => setGrid(Array(TOTAL_PIXELS).fill("#ffffff"))}
          className="px-4 py-2 rounded font-medium bg-gray-200"
        >
          Clear
        </button>
      </div>

      {/* Canvas */}
      <div
        className="border border-gray-400"
        style={{
          display: "grid",
          gridTemplateColumns: `repeat(${GRID_SIZE}, 1fr)`,
          width: 512,
          height: 512,
          userSelect: "none",
        }}
        onMouseLeave={() => setIsPainting(false)}
      >
        {grid.map((cellColor, i) => (
          <div
            key={i}
            style={{ backgroundColor: cellColor }}
            onMouseDown={() => {
              setIsPainting(true);
              paintCell(i);
            }}
            onMouseEnter={() => {
              if (isPainting) paintCell(i);
            }}
            onMouseUp={() => setIsPainting(false)}
          />
        ))}
      </div>

      {/* Submit */}
      <button
        onClick={handleSubmit}
        className="px-6 py-3 bg-green-500 text-white rounded font-bold text-lg"
      >
        {submitted ? "Submitted! ✓" : "Submit to Pi"}
      </button>
    </div>
  );
}
