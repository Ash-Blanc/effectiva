import Icon from '@/components/ui/icon'
import MarkdownRenderer from '@/components/ui/typography/MarkdownRenderer'
import { useStore } from '@/store'
import type { ChatMessage } from '@/types/os'
import Videos from './Multimedia/Videos'
import Images from './Multimedia/Images'
import Audios from './Multimedia/Audios'
import { memo } from 'react'
import AgentThinkingLoader from './AgentThinkingLoader'

const formatTime = (timestamp?: string | number) => {
  if (!timestamp) return 'just now'
  const date = new Date(timestamp)
  const now = new Date()
  const diffMs = now.getTime() - date.getTime()
  const diffMins = Math.floor(diffMs / 60000)
  const diffHours = Math.floor(diffMs / 3600000)
  const diffDays = Math.floor(diffMs / 86400000)
  
  if (diffMins < 1) return 'just now'
  if (diffMins < 60) return `${diffMins}m ago`
  if (diffHours < 24) return `${diffHours}h ago`
  if (diffDays < 7) return `${diffDays}d ago`
  return date.toLocaleDateString()
}

interface MessageProps {
  message: ChatMessage
}

const MessageActions = memo(({ message, onCopy }: { message: ChatMessage; onCopy: () => void }) => (
  <div className="flex items-center gap-2 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
    <button
      onClick={onCopy}
      className="p-1.5 rounded-lg hover:bg-gray-100 transition-colors duration-200"
      title="Copy message"
    >
      <Icon type="copy" size="xs" className="text-gray-500" />
    </button>
    {message.streamingError && (
      <button
        onClick={() => window.location.reload()}
        className="p-1.5 rounded-lg hover:bg-gray-100 transition-colors duration-200"
        title="Retry"
      >
        <Icon type="refresh" size="xs" className="text-gray-500" />
      </button>
    )}
  </div>
))

MessageActions.displayName = 'MessageActions'

const AgentMessage = ({ message }: MessageProps) => {
  const { streamingErrorMessage } = useStore()
  
  const handleCopy = () => {
    if (message.content) {
      navigator.clipboard.writeText(message.content)
    }
  }

  let messageContent
  if (message.streamingError) {
    messageContent = (
      <div className="agent-message">
        <div className="flex items-center gap-2 mb-2">
          <Icon type="error" size="sm" className="text-red-500" />
          <span className="text-sm font-medium text-red-600">Error</span>
        </div>
        <p className="text-red-600">
          Oops! Something went wrong while streaming.{' '}
          {streamingErrorMessage ? (
            <>{streamingErrorMessage}</>
          ) : (
            'Please try refreshing the page or try again later.'
          )}
        </p>
      </div>
    )
  } else if (message.content) {
    messageContent = (
      <div className="agent-message">
        <div className="flex flex-col gap-4">
          <MarkdownRenderer className="prose prose-sm max-w-none">
            {message.content}
          </MarkdownRenderer>
          {message.videos && message.videos.length > 0 && (
            <Videos videos={message.videos} />
          )}
          {message.images && message.images.length > 0 && (
            <Images images={message.images} />
          )}
          {message.audio && message.audio.length > 0 && (
            <Audios audio={message.audio} />
          )}
        </div>
      </div>
    )
  } else if (message.response_audio) {
    if (!message.response_audio.transcript) {
      messageContent = (
        <div className="agent-message">
          <div className="mt-2 flex items-center justify-center py-4">
            <AgentThinkingLoader />
          </div>
        </div>
      )
    } else {
      messageContent = (
        <div className="agent-message">
          <div className="flex flex-col gap-4">
            <MarkdownRenderer className="prose prose-sm max-w-none">
              {message.response_audio.transcript}
            </MarkdownRenderer>
            {message.response_audio.content && message.response_audio && (
              <Audios audio={[message.response_audio]} />
            )}
          </div>
        </div>
      )
    }
  } else {
    messageContent = (
      <div className="agent-message">
        <div className="mt-2 flex items-center justify-center py-4">
          <AgentThinkingLoader />
        </div>
      </div>
    )
  }

  return (
    <div className="group relative flex flex-row items-start gap-4 font-geist">
      <div className="flex-shrink-0">
        <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center shadow-lg">
          <Icon type="agent" size="sm" className="text-white" />
        </div>
      </div>
      <div className="flex flex-col gap-2 flex-1">
        <div className="flex items-center gap-2">
          <span className="text-sm font-medium text-gray-700">AI Assistant</span>
          <span className="text-xs text-gray-500">
            {formatTime(message.timestamp)}
          </span>
        </div>
        {messageContent}
        <MessageActions message={message} onCopy={handleCopy} />
      </div>
    </div>
  )
}

const UserMessage = memo(({ message }: MessageProps) => {
  const handleCopy = () => {
    if (message.content) {
      navigator.clipboard.writeText(message.content)
    }
  }

  return (
    <div className="group relative flex items-start gap-4 pt-4 text-start max-md:break-words">
      <div className="flex-shrink-0">
        <div className="w-10 h-10 rounded-full bg-gradient-to-br from-green-500 to-emerald-600 flex items-center justify-center shadow-lg">
          <Icon type="user" size="sm" className="text-white" />
        </div>
      </div>
      <div className="flex flex-col gap-2 flex-1">
        <div className="flex items-center gap-2 justify-end">
          <span className="text-xs text-gray-500">
            {formatTime(message.timestamp)}
          </span>
          <span className="text-sm font-medium text-gray-700">You</span>
        </div>
        <div className="user-message">
          <p className="text-gray-800 leading-relaxed">{message.content}</p>
        </div>
        <MessageActions message={message} onCopy={handleCopy} />
      </div>
    </div>
  )
})

AgentMessage.displayName = 'AgentMessage'
UserMessage.displayName = 'UserMessage'
export { AgentMessage, UserMessage }
