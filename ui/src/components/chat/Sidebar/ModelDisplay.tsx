'use client'
import { useStore } from '@/store'

const ModelDisplay = ({ model }: { model: string }) => {
    return (
        <div className="rounded-xl border border-primary/15 bg-accent p-3">
            <div className="text-xs font-medium uppercase text-muted">
                Model: {model}
            </div>
        </div>
    )
}

export default ModelDisplay
