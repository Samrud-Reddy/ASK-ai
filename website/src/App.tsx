import { useState } from "react";
import "./App.css";
import { Input, NativeSelect } from "@mantine/core";
import { IconSend2 } from "@tabler/icons-react";
import { handleSubmit } from "./handleSubmit";

function App() {
    const [question, setQuestion] = useState<string>("");

    return (
        <div className="wrapperDiv">
            <h2 className="title">Ask AI Anything</h2>
            <div className="inputStuff">
                <NativeSelect size="lg" className="subjectSelect" data={["Chemistry", "Physics", "Biology", "Comp Sci"]} />
                <Input
                    className="askInput"
                    placeholder="Ask AI Anything..."
                    rightSection={<IconSend2 className="sendIcon" onClick={() => console.log("kk")} />}
                    size="lg"
                    value={question}
                    onChange={(e) => {
                        setQuestion(e.target.value);
                    }}
                    onKeyUp={(e) => {
                        if (e.key == "Enter") {
                            handleSubmit();
                            setQuestion("");
                        }
                    }}
                />
            </div>
        </div>
    );
}

export default App;
