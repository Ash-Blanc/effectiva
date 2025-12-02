'use client'

import ChatInput from './ChatInput'
import MessageArea from './MessageArea'
const ChatArea = () => {
  return (
    <main className="relative flex flex-grow flex-col rounded-2xl bg-gradient-to-br from-background/90 via-background/80 to-background/70 backdrop-blur-sm border border-gray-200/30 shadow-xl">
      <div className="flex flex-grow flex-col overflow-hidden">
        <MessageArea />
        <div className="chat-input-container">
          <div className="px-6 py-4">
            <ChatInput />
          </div>
        </div>
      </div>
    </main>
  )
}

export default ChatArea
