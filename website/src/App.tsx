import { useState } from "react";
import "./App.css";
import { NativeSelect, TextInput } from "@mantine/core";
import { IconSend2 } from "@tabler/icons-react";
import { handleSubmit } from "./handleSubmit";
import { useHover } from "@mantine/hooks";

function App() {
    const [question, setQuestion] = useState<string>("");
    const subjectList: string[] = ["Chemistry", "Physics", "Biology", "Comp Sci"];
    const { hovered, ref } = useHover();

    return (
        <div className="wrapperDiv">
            <h2 className="title">Ask AI Anything</h2>
            <div className="inputStuff">
                <NativeSelect size="lg" className="subjectSelect" data={subjectList} />
                <TextInput
                    className="askInput"
                    placeholder="Ask AI Anything..."
                    rightSection={
                        <div className="iconDiv" ref={ref}>
                            <IconSend2
                                stroke={hovered ? 2 : 1}
                                className="sendIcon"
                                onClick={() => handleSubmit(question)}
                            />
                        </div>
                    }
                    rightSectionPointerEvents="all"
                    size="lg"
                    value={question}
                    onChange={(e) => {
                        setQuestion(e.currentTarget.value);
                    }}
                    onKeyUp={(e) => {
                        if (e.key == "Enter") {
                            handleSubmit(question);
                            setQuestion("");
                        }
                    }}
                />
            </div>
        </div>
    );
}

export default App;
