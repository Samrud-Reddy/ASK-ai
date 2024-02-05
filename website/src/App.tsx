import { useState } from "react";
import "./App.css";
import { NativeSelect, TextInput } from "@mantine/core";
import { IconSend2 } from "@tabler/icons-react";
import { handleSubmit } from "./handleSubmit";
import { useHover } from "@mantine/hooks";

const App = () => {
    const [question, setQuestion] = useState<string>("");
    const [subject, setSubject] = useState<string>("Chemistry"); // setting chemistry as default cuz it's the hardest
    const [prevChatArray, setPrevChatArray] = useState<string[]>([]);
    const subjectList: string[] = ["Chemistry", "Physics", "Biology", "Comp Sci"];
    const { hovered, ref } = useHover();

    return (
        <div className="wrapperDiv">
            <h2 className="title">Ask AI Anything</h2>
            <div className="chatBox">
                {prevChatArray.map((msg: string, index: number) => {
                    if (index % 2 == 0) {
                        return <p key={msg + Math.random()}>You: {msg}</p>;
                    } else {
                        return <p key={msg + Math.random()}>Ask AI: {msg}</p>;
                    }
                })}
            </div>
            <div className="inputStuff">
                <NativeSelect
                    value={subject}
                    size="lg"
                    className="subjectSelect"
                    data={subjectList}
                    onChange={(e) => {
                        setSubject(e.currentTarget.value);
                    }}
                />
                <TextInput
                    className="askInput"
                    placeholder="Ask AI Anything..."
                    rightSection={
                        <div className="iconDiv" ref={ref}>
                            <IconSend2
                                stroke={hovered ? 2 : 1}
                                className="sendIcon"
                                onClick={async () => {
                                    const questionAsked = question;
                                    setQuestion("");
                                    setPrevChatArray((prevChatArray) => [...prevChatArray, questionAsked]);
                                    const response = await handleSubmit(questionAsked, subject, prevChatArray);
                                    console.log("RESPONSE IS " + response);
                                    setPrevChatArray((prevChatArray) => [...prevChatArray, response]);
                                }}
                            />
                        </div>
                    }
                    rightSectionPointerEvents="all"
                    size="lg"
                    value={question}
                    onChange={(e) => {
                        setQuestion(e.currentTarget.value);
                    }}
                    onKeyUp={async (e) => {
                        if (e.key == "Enter") {
                            const questionAsked = question;
                            setQuestion("");
                            setPrevChatArray((prevChatArray) => [...prevChatArray, questionAsked]);
                            const response = await handleSubmit(questionAsked, subject, prevChatArray);
                            console.log("RESPONSE IS " + response);
                            setPrevChatArray((prevChatArray) => [...prevChatArray, response]);
                        }
                    }}
                />
            </div>
        </div>
    );
};

export default App;
