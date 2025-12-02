'use client'
import { useState, useEffect } from 'react'
import { useStore } from '@/store'
import { Button } from '@/components/ui/button'

const Endpoint = () => {
    const { selectedEndpoint, setSelectedEndpoint, setIsEndpointActive } = useStore()
    const [endpoint, setEndpoint] = useState(selectedEndpoint || 'http://localhost:7777')

    useEffect(() => {
        if (selectedEndpoint) {
            setEndpoint(selectedEndpoint)
        }
    }, [selectedEndpoint])

    const handleConnect = () => {
        setSelectedEndpoint(endpoint)
        setIsEndpointActive(true)
    }

    return (
        <div className="flex flex-col items-start gap-2">
            <div className="text-xs font-medium uppercase text-primary">
                Endpoint
            </div>
            <div className="flex w-full items-center gap-1">
                <input
                    type="text"
                    value={endpoint}
                    onChange={(e) => setEndpoint(e.target.value)}
                    placeholder="http://localhost:7777"
                    className="flex h-9 w-full items-center rounded-xl border border-primary/15 bg-accent p-3 text-xs font-medium text-muted"
                />
                <Button
                    variant="ghost"
                    size="sm"
                    onClick={handleConnect}
                    className="h-9"
                >
                    Connect
                </Button>
            </div>
        </div>
    )
}

export default Endpoint
