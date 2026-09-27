// [Incremental Update: MIME-Aware Converter wired to Event Bus]
import React from 'react';

interface FilePayload {
  name: string;
  mimeType: string;
  size: number;
}

export const RenderConverterControls = ({ file }: { file: FilePayload }) => {
  if (file.mimeType.startsWith('image/')) {
    return (
      <div className="conversion-panel">
        <label>Target Format:</label>
        <select id="targetFormat">
          <option value="webp">WEBP (Optimized Web)</option>
          <option value="png">PNG (Lossless)</option>
          <option value="jpg">JPG (Standard Image)</option>
          <option value="svg">SVG (Vector Trace)</option>
        </select>
        <div className="slider-group">
          <label>Quality Percentage:</label>
          <input type="range" min="10" max="100" defaultValue="85" />
          <label>Resize Width (px):</label>
          <input type="number" placeholder="Auto" />
        </div>
      </div>
    );
  }

  if (file.mimeType.startsWith('video/')) {
    return (
      <div className="conversion-panel">
        <label>Target Format:</label>
        <select id="targetFormat">
          <option value="mp4">MP4 (H.264 / AAC)</option>
          <option value="webm">WebM (VP9 / Opus)</option>
          <option value="mkv">MKV (Matroska Container)</option>
        </select>
        <div className="slider-group">
          <label>Target Resolution:</label>
          <select>
            <option value="1080p">1080p (Full HD)</option>
            <option value="720p">720p (HD)</option>
            <option value="480p">480p (SD)</option>
          </select>
          <label>Video Bitrate (Kbps):</label>
          <input type="number" defaultValue="2500" />
        </div>
      </div>
    );
  }

  return (
    <div className="conversion-panel">
      <label>Target Format:</label>
      <select id="targetFormat">
        <option value="pdf">PDF Document</option>
        <option value="docx">Microsoft Word (DOCX)</option>
        <option value="txt">Plain Text (TXT)</option>
      </select>
      <div className="toggle-group">
        <label><input type="checkbox" /> Enable Optical Character Recognition (OCR)</label>
      </div>
    </div>
  );
};
