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
    const [history, setHistory] = useState<string[]>([]);
    const subjectList: string[] = ["Chemistry", "Physics", "Biology", "Comp Sci"];
    const { hovered, ref } = useHover();

    const handleSubmission = async () => {
        const questionAsked = question.trim();
        const historyToPassIn = [...history];
        console.log(historyToPassIn);
        setQuestion("");
        setPrevChatArray((prevChatArray) => [...prevChatArray, questionAsked]);
        setCanSend(false);
        const response = await handleSubmit(questionAsked, subject, historyToPassIn);
        if (response instanceof Error) {
            setPrevChatArray((prevChatArray) => [...prevChatArray, "Oops an error has occured"]);
        } else {
            setPrevChatArray((prevChatArray) => [...prevChatArray, response]);
            setHistory([...history, questionAsked, response]);
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
                    size="md"
                    className="subjectSelect"
                    data={subjectList}
                    onChange={(e) => {
                        setSubject(e.currentTarget.value);
                    }}
                />
                <Textarea
                    className="askInput"
                    placeholder="Ask AI Anything..."
                    autosize
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
                    size="md"
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
