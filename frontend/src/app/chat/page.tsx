import dynamic from 'next/dynamic';
import { Metadata } from 'next';

// Dynamically import the ChatUI component to ensure it's only rendered on the client side
const ChatUI = dynamic(() => import('@/components/chat/ChatUI'), {
  ssr: false,
  loading: () => <div className="flex justify-center items-center h-64">
    <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
  </div>
});

export const metadata: Metadata = {
  title: 'Chat - Todo App',
  description: 'AI-powered chat assistant for your tasks',
};

export default function ChatPage() {
  return (
    <div className="container mx-auto px-4 py-8 max-w-4xl">
      <div className="mb-8 text-center">
        <h1 className="text-3xl font-bold text-gray-800 mb-2">AI Assistant</h1>
        <p className="text-gray-600">Chat with our intelligent assistant to manage your tasks</p>
      </div>

      <div className="bg-white rounded-xl shadow-lg overflow-hidden border border-gray-200">
        <div className="p-4 bg-gradient-to-r from-blue-600 to-indigo-600 text-white">
          <h2 className="text-xl font-semibold">Task Management Assistant</h2>
        </div>
        <div className="p-2 h-[500px]">
          <ChatUI />
        </div>
      </div>

      <div className="mt-6 text-center text-sm text-gray-500">
        <p>Your conversations are secure and private</p>
      </div>
    </div>
  );
}