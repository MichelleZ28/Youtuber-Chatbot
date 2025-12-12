import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Box, Button, Container, Flex, Heading, HStack, Input, Text, VStack, Avatar, useColorModeValue, Spinner, Badge, chakra } from '@chakra-ui/react';
import { FaYoutube, FaUser } from 'react-icons/fa';
function App() {
    const [channelUrl, setChannelUrl] = useState('');
    const [isChatStarted, setIsChatStarted] = useState(false);
    const [messages, setMessages] = useState([]);
    const [inputMessage, setInputMessage] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [channelInfo, setChannelInfo] = useState(null);
    const [startupHint, setStartupHint] = useState(null);
    const bubbleBgUser = useColorModeValue('gray.50', 'gray.700');
    const bubbleBgBot = useColorModeValue('red.500', 'red.400');
    const bubbleBorderUser = useColorModeValue('gray.200', 'gray.600');
    const surfaceBg = useColorModeValue('white', 'gray.800');
    const surfaceBorder = useColorModeValue('gray.100', 'gray.700');
    const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
    const extractChannelIdentifier = (input) => {
        const trimmed = input.trim();
        if (!trimmed) {
            return null;
        }
        // If the input isn't a URL, assume it's already an identifier or handle.
        if (!/^https?:\/\//i.test(trimmed)) {
            return trimmed;
        }
        try {
            const url = new URL(trimmed);
            const segments = url.pathname.split('/').filter(Boolean);
            if (!segments.length) {
                return null;
            }
            const [firstSegment, secondSegment] = segments;
            if (firstSegment.startsWith('@')) {
                return firstSegment;
            }
            if ((firstSegment === 'channel' || firstSegment === 'c' || firstSegment === 'user') && secondSegment) {
                return secondSegment;
            }
            return null;
        }
        catch {
            // If URL parsing fails, fall back to the original trimmed value.
            return trimmed;
        }
    };
    const renderAvatar = (sender) => {
        if (sender === 'user') {
            return (_jsx(Avatar, { icon: _jsx(FaUser, {}), name: "You", size: "md", bg: "green.100", color: "green.700", fontWeight: "semibold" }));
        }
        if (channelInfo?.thumbnail) {
            return _jsx(Avatar, { src: channelInfo.thumbnail, name: channelInfo.title || 'Channel', size: "md" });
        }
        // Get first letter of channel title or use 'YT' as fallback
        const firstLetter = channelInfo?.title ? channelInfo.title.charAt(0).toUpperCase() : 'YT';
        return (_jsx(Avatar, { name: firstLetter, size: "md", bg: "red.100", color: "red.700", fontWeight: "semibold" }));
    };
    const handleStartChat = async (e) => {
        e.preventDefault();
        if (!channelUrl.trim())
            return;
        const identifier = extractChannelIdentifier(channelUrl);
        if (!identifier) {
            setIsChatStarted(true);
            setChannelInfo({ title: channelUrl });
            setMessages([
                {
                    id: 1,
                    text: `Chat started with YouTube channel: ${channelUrl}. How can I help you today?`,
                    sender: 'bot'
                }
            ]);
            return;
        }
        setIsLoading(true);
        setStartupHint('Connecting to the server...');
        const warmupTimer = window.setTimeout(() => {
            setStartupHint('This can take a few seconds if the server is waking up...');
        }, 2500);
        try {
            // First, fetch channel info so avatar and header render immediately
            const response = await fetch(`${API_BASE_URL}/api/channels/${encodeURIComponent(identifier)}`);
            if (response.ok) {
                const data = await response.json();
                setChannelInfo(data);
            }
            else {
                console.error('Failed to fetch channel info');
                setChannelInfo({ title: channelUrl });
            }
        }
        catch (error) {
            console.error('Error fetching channel info:', error);
            setChannelInfo({ title: channelUrl });
        }
        finally {
            clearTimeout(warmupTimer);
            setIsLoading(false);
            setStartupHint(null);
            setIsChatStarted(true);
            // Add a welcome message when chat starts
            setMessages([
                {
                    id: 1,
                    text: `Chat started with YouTube channel: ${channelUrl}. How can I help you today?`,
                    sender: 'bot'
                }
            ]);
        }
    };
    const handleSendMessage = async (e) => {
        e.preventDefault();
        if (!inputMessage.trim() || isLoading)
            return;
        // Add user message
        const newUserMessage = {
            id: Date.now(),
            text: inputMessage,
            sender: 'user'
        };
        const updatedMessages = [...messages, newUserMessage];
        setMessages(updatedMessages);
        setInputMessage('');
        setIsLoading(true);
        try {
            // Send message to backend
            const response = await fetch(`${API_BASE_URL}/api/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    youtube_url: channelUrl,
                    message: inputMessage,
                    chat_history: updatedMessages
                        .filter(msg => msg.sender === 'user' || msg.sender === 'bot')
                        .map(msg => ({
                        role: msg.sender === 'user' ? 'user' : 'assistant',
                        content: msg.text
                    }))
                }),
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            if (data.channel_info) {
                setChannelInfo(data.channel_info);
            }
            // Remove loading message and add AI response
            setMessages(prev => ([
                ...prev,
                {
                    id: Date.now() + 2,
                    text: data.response || "I'm not sure how to respond to that.",
                    sender: 'bot'
                }
            ]));
        }
        catch (error) {
            console.error('Error:', error);
            setMessages(prev => ([
                ...prev,
                {
                    id: Date.now() + 2,
                    text: "Sorry, I encountered an error processing your request. Please try again.",
                    sender: 'bot'
                }
            ]));
        }
        finally {
            setIsLoading(false);
        }
    };
    return (_jsxs(Flex, { minH: "100vh", direction: "column", bg: useColorModeValue('gray.50', 'gray.900'), children: [_jsx(Box, { as: "header", bg: "red.600", color: "white", py: 5, boxShadow: "sm", children: _jsx(Container, { maxW: "5xl", children: _jsxs(Flex, { align: "center", children: [_jsx(Box, { as: FaYoutube, boxSize: "80px", color: "white", mr: 3 }), _jsx(Heading, { size: "lg", fontWeight: "semibold", children: "YouTuber Chatbot" })] }) }) }), _jsx(Container, { maxW: "5xl", flex: "1", py: 8, children: !isChatStarted ? (_jsx(Flex, { align: "center", justify: "center", h: "full", children: _jsx(chakra.form, { onSubmit: handleStartChat, bg: surfaceBg, borderRadius: "2xl", boxShadow: "lg", p: 8, borderWidth: "1px", borderColor: surfaceBorder, maxW: "md", w: "full", children: _jsxs(VStack, { spacing: 6, align: "stretch", children: [_jsxs("div", { children: [_jsx(Heading, { size: "md", mb: 2, children: "Enter a YouTube channel to begin" }), _jsx(Text, { color: "gray.500", children: "Paste a channel URL or handle to start chatting in their style." })] }), _jsxs(VStack, { align: "stretch", spacing: 2, children: [_jsx(chakra.label, { htmlFor: "channelUrl", fontWeight: "medium", children: "YouTube Channel URL or Handle" }), _jsx(Input, { id: "channelUrl", value: channelUrl, onChange: (e) => setChannelUrl(e.target.value), placeholder: "e.g. https://www.youtube.com/@NeetCode", size: "lg", required: true })] }), _jsx(Button, { type: "submit", colorScheme: "red", size: "lg", borderRadius: "lg", isLoading: isLoading, loadingText: "Starting chat", children: "Start Chat" }), isLoading && !isChatStarted && startupHint && (_jsx(Text, { fontSize: "sm", color: "gray.500", textAlign: "center", children: startupHint }))] }) }) })) : (_jsxs(Flex, { direction: "column", h: "full", gap: 6, children: [_jsx(Button, { alignSelf: "flex-end", variant: "ghost", size: "sm", onClick: () => {
                                setIsChatStarted(false);
                                setChannelInfo(null);
                                setMessages([]);
                                setChannelUrl('');
                            }, children: "\u2190 Change Channel" }), channelInfo && (_jsxs(Flex, { align: "center", gap: 4, bg: surfaceBg, borderRadius: "2xl", borderWidth: "1px", borderColor: surfaceBorder, p: 5, boxShadow: "sm", children: [renderAvatar('bot'), _jsxs(Box, { children: [_jsx(Heading, { size: "md", children: channelInfo.title || 'Channel assistant' }), _jsxs(HStack, { spacing: 3, mt: 1, color: "gray.500", children: [_jsxs(Text, { fontSize: "sm", children: ["You can start chatting with ", channelInfo.title || 'the Channel assistant'] }), channelInfo.subscriber_count && (_jsxs(Badge, { colorScheme: "red", children: [Number(channelInfo.subscriber_count).toLocaleString(), " subs"] }))] })] })] })), _jsx(Box, { flex: "1", bg: surfaceBg, borderRadius: "3xl", borderWidth: "1px", borderColor: surfaceBorder, boxShadow: "sm", p: 5, overflowY: "auto", minH: "0", children: _jsxs(VStack, { spacing: 5, align: "stretch", children: [messages.map((message) => (_jsx(Flex, { justify: message.sender === 'user' ? 'flex-end' : 'flex-start', children: _jsxs(HStack, { spacing: 4, align: "flex-end", flexDir: "row", maxW: "full", children: [renderAvatar(message.sender), _jsx(Box, { bg: message.sender === 'user' ? bubbleBgUser : bubbleBgBot, color: message.sender === 'user' ? 'gray.800' : 'white', borderRadius: "3xl", borderBottomLeftRadius: message.sender === 'user' ? '3xl' : 0, borderBottomRightRadius: message.sender === 'user' ? 0 : '3xl', px: 5, py: 3, boxShadow: "sm", borderWidth: message.sender === 'user' ? '1px' : 0, borderColor: message.sender === 'user' ? bubbleBorderUser : 'transparent', maxW: "lg", children: _jsx(chakra.p, { whiteSpace: "pre-wrap", fontSize: "sm", lineHeight: "1.6", children: message.text }) })] }) }, message.id))), isLoading && (_jsx(Flex, { justify: "flex-start", children: _jsxs(HStack, { spacing: 4, flexDir: "row", align: "flex-end", children: [renderAvatar('bot'), _jsxs(HStack, { bg: "red.50", color: "red.600", borderRadius: "3xl", borderBottomLeftRadius: 0, px: 5, py: 3, boxShadow: "sm", children: [_jsx(Spinner, { size: "sm", speed: "0.6s" }), _jsx(Text, { fontSize: "sm", children: "Thinking..." })] })] }) }))] }) }), _jsxs(Flex, { as: "form", onSubmit: handleSendMessage, gap: 3, align: "center", children: [_jsx(Input, { value: inputMessage, onChange: (e) => setInputMessage(e.target.value), placeholder: "Ask something about the channel's content...", size: "lg", isDisabled: isLoading, flex: "1" }), _jsx(Button, { type: "submit", size: "lg", colorScheme: "red", isDisabled: isLoading, borderRadius: "lg", children: "Send" })] })] })) })] }));
}
export default App;
