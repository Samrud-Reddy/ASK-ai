import { useState } from "react";
import "./App.css";
import { NativeSelect, Textarea } from "@mantine/core";
import { IconSend2 } from "@tabler/icons-react";
import { handleSubmit } from "./handleSubmit";
import { useHover } from "@mantine/hooks";

const App = () => {
    const [question, setQuestion] = useState<string>("");
    const [subject, setSubject] = useState<string>("Chemistry"); // setting chemistry as default cuz it's the hardest
    const [prevChatArray, setPrevChatArray] = useState<string[]>([]);
    const [canSend, setCanSend] = useState<boolean>(true);
    const subjectList: string[] = ["Chemistry", "Physics", "Biology", "Comp Sci"];
    const { hovered, ref } = useHover();

    const handleSubmission = async () => {
        const questionAsked = question.trim();
        setQuestion("");
        setPrevChatArray((prevChatArray) => [...prevChatArray, questionAsked]);
        setCanSend(false);
        const response = await handleSubmit(questionAsked, subject);
        if (response instanceof Error){
            setPrevChatArray((prevChatArray) => [...prevChatArray, "Oops an error has occured"]);
        } else {
            setPrevChatArray((prevChatArray) => [...prevChatArray, response]);
        }
        
        setCanSend(true);
    };

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
                <Textarea
                    className="askInput"
                    placeholder="Ask AI Anything..."
                    rightSection={
                        <div className="iconDiv" ref={ref}>
                            <IconSend2
                                stroke={hovered ? 2 : 1}
                                className="sendIcon"
                                onClick={() => {
                                    if (question != "" && canSend) {
                                        handleSubmission();
                                    }
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
                        if (e.key == "Enter" && question.trim() != "" && canSend && !e.shiftKey) {
                            handleSubmission();
                        }
                    }}
                />
            </div>
        </div>
    );
};

export default App;
