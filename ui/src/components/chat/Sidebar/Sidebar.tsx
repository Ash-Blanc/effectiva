'use client'
import { useState, useEffect } from 'react'
import Link from 'next/link'
import { motion } from 'framer-motion'
import { Button } from '@/components/ui/button'
import { Skeleton } from '@/components/ui/skeleton'
import Icon from '@/components/ui/icon'
import { useStore } from '@/store'
import SidebarHeader from './SidebarHeader'
import NewChatButton from './NewChatButton'
import AuthToken from './AuthToken'
import { ModeSelector } from './ModeSelector'
import { EntitySelector } from './EntitySelector'
import ModelDisplay from './ModelDisplay'
import Sessions from './Sessions'
import Endpoint from './Endpoint'

const NavLink = ({ href, children }: { href: string; children: React.ReactNode }) => {
    return (
        <Link href={href} passHref>
            <Button
                variant="ghost"
                className="h-9 w-full justify-start rounded-xl text-xs font-medium uppercase text-muted hover:text-primary"
            >
                {children}
            </Button>
        </Link>
    )
}

const Sidebar = ({ hasEnvToken, envToken }: { hasEnvToken?: boolean; envToken?: string }) => {
    const { isEndpointActive, isEndpointLoading, selectedModel, mode } = useStore()
    const [isCollapsed, setIsCollapsed] = useState(false)
    const [isMounted, setIsMounted] = useState(false)

    const agentId = mode === 'agent' ? selectedModel : null
    const teamId = mode === 'team' ? selectedModel : null

    useEffect(() => {
        setIsMounted(true)
    }, [])

    return (
        <motion.aside
            className="relative flex h-screen shrink-0 grow-0 flex-col overflow-hidden px-2 py-3 font-dmmono"
            initial={{ width: '16rem' }}
            animate={{ width: isCollapsed ? '2.5rem' : '16rem' }}
            transition={{ type: 'spring', stiffness: 300, damping: 30 }}
        >
            <motion.button
                onClick={() => setIsCollapsed(!isCollapsed)}
                className="absolute right-2 top-2 z-10 p-1"
                aria-label={isCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
                type="button"
                whileTap={{ scale: 0.95 }}
            >
                <Icon
                    type="sheet"
                    size="xs"
                    className={`transform ${isCollapsed ? 'rotate-180' : 'rotate-0'}`}
                />
            </motion.button>
            <motion.div
                className="w-60 space-y-5"
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: isCollapsed ? 0 : 1, x: isCollapsed ? -20 : 0 }}
                transition={{ duration: 0.3, ease: 'easeInOut' }}
                style={{
                    pointerEvents: isCollapsed ? 'none' : 'auto'
                }}
            >
                <SidebarHeader />
                <NewChatButton />
                {isMounted && (
                    <>
                        <Endpoint />
                        <AuthToken hasEnvToken={hasEnvToken} envToken={envToken} />
                        {isEndpointActive && (
                            <>
                                <motion.div
                                    className="flex w-full flex-col items-start gap-2"
                                    initial={{ opacity: 0 }}
                                    animate={{ opacity: 1 }}
                                    transition={{ duration: 0.5, ease: 'easeInOut' }}
                                >
                                    <div className="text-xs font-medium uppercase text-primary">
                                        Mode
                                    </div>
                                    {isEndpointLoading ? (
                                        <div className="flex w-full flex-col gap-2">
                                            {Array.from({ length: 3 }).map((_, index) => (
                                                <Skeleton
                                                    key={index}
                                                    className="h-9 w-full rounded-xl"
                                                />
                                            ))}
                                        </div>
                                    ) : (
                                        <>
                                            <ModeSelector />
                                            <EntitySelector />
                                            {selectedModel && (agentId || teamId) && (
                                                <ModelDisplay model={selectedModel} />
                                            )}
                                        </>
                                    )}
                                </motion.div>
                                <NavLink href="/agents">
                                    <Icon type="settings" size="xs" className="mr-2" />
                                    Agent Config
                                </NavLink>
                                <Sessions />
                            </>
                        )}
                    </>
                )}
            </motion.div>
        </motion.aside>
    )
}

export default Sidebar
