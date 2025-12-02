'use client'
import { useState, useEffect } from 'react'
import { toast } from 'sonner'
import { TextArea } from '@/components/ui/textarea'
import { Button } from '@/components/ui/button'
import { useStore } from '@/store'
import useAIChatStreamHandler from '@/hooks/useAIStreamHandler'
import { useQueryState } from 'nuqs'
import Icon from '@/components/ui/icon'

const ChatInput = () => {
  const { chatInputRef } = useStore()

  const { handleStreamResponse } = useAIChatStreamHandler()
  const [selectedAgent] = useQueryState('agent')
  const [teamId] = useQueryState('team')
  const [inputMessage, setInputMessage] = useState('')
  const [charCount, setCharCount] = useState(0)
  const isStreaming = useStore((state) => state.isStreaming)
  
  const MAX_CHARS = 4000

  useEffect(() => {
    setCharCount(inputMessage.length)
  }, [inputMessage])

  const handleSubmit = async () => {
    if (!inputMessage.trim()) return

    const currentMessage = inputMessage
    setInputMessage('')

    try {
      await handleStreamResponse(currentMessage)
    } catch (error) {
      toast.error(
        `Error in handleSubmit: ${
          error instanceof Error ? error.message : String(error)
        }`
      )
    }
  }

  const isDisabled = !(selectedAgent || teamId) || !inputMessage.trim() || isStreaming
  const charPercentage = (charCount / MAX_CHARS) * 100

  return (
    <div className="relative mx-auto flex w-full max-w-2xl flex-col gap-3">
      <div className="relative">
        <TextArea
          placeholder="Ask anything..."
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          onKeyDown={(e) => {
            if (
              e.key === 'Enter' &&
              !e.nativeEvent.isComposing &&
              !e.shiftKey &&
              !isStreaming
            ) {
              e.preventDefault()
              handleSubmit()
            }
          }}
          className="w-full border-2 border-gray-200 bg-white/90 backdrop-blur-sm px-4 py-3 text-sm text-gray-900 placeholder-gray-500 focus:border-blue-400 focus:ring-0 focus:outline-none transition-all duration-200 resize-none shadow-sm hover:shadow-md"
          disabled={isDisabled}
          ref={chatInputRef}
        />
        
        {/* Character counter */}
        <div className="absolute bottom-2 right-2 text-xs text-gray-400">
          {charCount}/{MAX_CHARS}
        </div>
        
        {/* Progress bar */}
        {charPercentage > 80 && (
          <div
            className="absolute bottom-0 left-0 h-0.5 bg-gradient-to-r from-green-400 via-yellow-400 to-red-400 transition-all duration-300"
            style={{ width: `${Math.min(charPercentage, 100)}%` }}
          />
        )}
      </div>
      
      {/* Keyboard shortcut hint */}
      <div className="flex items-center justify-between text-xs text-gray-500">
        <div className="flex items-center gap-2">
          <kbd className="px-2 py-1 bg-gray-100 rounded text-xs font-mono">Enter</kbd>
          <span>to send</span>
          <kbd className="px-2 py-1 bg-gray-100 rounded text-xs font-mono">Shift</span> + <span>Enter</span>
          <span>for new line</span>
        </div>
        {isStreaming && (
          <div className="typing-indicator">
            <div className="typing-dot" style={{ '--delay': '0' } as React.CSSProperties} />
            <div className="typing-dot" style={{ '--delay': '1' } as React.CSSProperties} />
            <div className="typing-dot" style={{ '--delay': '2' } as React.CSSProperties} />
            <span className="ml-2">AI is thinking...</span>
          </div>
        )}
      </div>
      
      <Button
        onClick={handleSubmit}
        disabled={isDisabled}
        size="icon"
        className="h-12 w-12 rounded-xl bg-gradient-to-br from-blue-500 to-indigo-600 text-white shadow-lg hover:shadow-xl hover:from-blue-600 hover:to-indigo-700 transition-all duration-200 transform hover:scale-105"
      >
        <Icon type="send" color="white" size="md" />
      </Button>
    </div>
  )
}

export default ChatInput
