import React from "react";
import Row from "react-bootstrap/Row";

interface ParagraphProps {
  paragraph: string;
  tag: string;
}

function Paragraph({ paragraph, tag }: ParagraphProps) {
  return (
    <div className="paragraph">
      <div>{paragraph}</div>
      <div className="tag">{tag}</div>
    </div>
  );
}

export default Paragraph;
