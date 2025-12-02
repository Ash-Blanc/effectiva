"use client";

import { useEffect, useState } from "react";
import Heading from "@/components/ui/typography/Heading";
import Paragraph from "@/components/ui/typography/Paragraph";

interface Optimizer {
  id: string;
  name: string;
  type: string;
  is_active: boolean;
}

interface ToonConfig {
  enabled: boolean;
  config_id: string | null;
}

interface Agent {
  agent_id: string;
  name: string;
  description: string;
  context: string;
  optimizers: Optimizer[];
  toon: ToonConfig;
  tools_count: number;
}

interface ApiResponse {
  agents: Agent[];
}

export default function AgentsPage() {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchAgents = async () => {
      try {
        const response = await fetch('http://localhost:7777/api/agents');
        if (!response.ok) {
          throw new Error(`Failed to fetch agents: ${response.statusText}`);
        }
        const data: ApiResponse = await response.json();
        setAgents(data.agents);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error occurred');
        console.error('Error fetching agents:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchAgents();
  }, []);

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen p-4">
        <Heading size={1} className="mb-4 text-center">
          Loading Agent Configurations...
        </Heading>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen p-4">
        <Heading size={1} className="mb-4 text-center text-red-600">
          Error Loading Agents
        </Heading>
        <Paragraph className="text-center text-gray-600">{error}</Paragraph>
        <Paragraph className="mt-4 text-sm text-center text-gray-500">
          Make sure the backend is running on http://localhost:7777
        </Paragraph>
      </div>
    );
  }

  return (
    <div className="flex flex-col items-center min-h-screen p-8 bg-background">
      <div className="w-full max-w-6xl">
        <Heading size={1} className="mb-2 text-center">
          Agent Configurations
        </Heading>
        <Paragraph className="text-lg text-center text-muted-foreground mb-8">
          View and manage your AI agents and their configurations
        </Paragraph>

        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {agents.map((agent) => (
            <div
              key={agent.agent_id}
              className="p-6 bg-card rounded-lg border shadow-sm hover:shadow-md transition-shadow"
            >
              <div className="mb-4">
                <Heading size={3} className="mb-2">
                  {agent.name}
                </Heading>
                <Paragraph className="text-sm text-muted-foreground">
                  {agent.description}
                </Paragraph>
              </div>

              <div className="space-y-3">
                {/* Context Badge */}
                <div className="flex items-center gap-2">
                  <span className="text-xs font-medium px-2 py-1 bg-primary/10 text-primary rounded">
                    {agent.context}
                  </span>
                </div>

                {/* Optimizers */}
                <div>
                  <p className="text-sm font-medium mb-1">Optimizers:</p>
                  {agent.optimizers.length > 0 ? (
                    <ul className="text-sm space-y-1">
                      {agent.optimizers.map((opt) => (
                        <li key={opt.id} className="flex items-center gap-2">
                          <span
                            className={`w-2 h-2 rounded-full ${
                              opt.is_active ? 'bg-green-500' : 'bg-gray-400'
                            }`}
                          />
                          <span className="text-muted-foreground">
                            {opt.type}
                          </span>
                        </li>
                      ))}
                    </ul>
                  ) : (
                    <Paragraph className="text-sm text-muted-foreground italic">
                      No optimizers configured
                    </Paragraph>
                  )}
                </div>

                {/* Toon Config */}
                <div>
                  <p className="text-sm font-medium mb-1">Toon Format:</p>
                  <div className="flex items-center gap-2">
                    <span
                      className={`w-2 h-2 rounded-full ${
                        agent.toon.enabled ? 'bg-green-500' : 'bg-gray-400'
                      }`}
                    />
                    <span className="text-sm text-muted-foreground">
                      {agent.toon.enabled ? 'Enabled' : 'Disabled'}
                    </span>
                  </div>
                </div>

                {/* Tools Count */}
                <div>
                  <p className="text-sm font-medium mb-1">Available Tools:</p>
                  <span className="text-sm text-muted-foreground">
                    {agent.tools_count} tools
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="mt-8 p-4 bg-muted/50 rounded-lg">
          <Paragraph className="text-sm text-center text-muted-foreground">
            💡 Tip: Use the optimizer and Toon endpoints in the backend API to
            configure agent settings.
          </Paragraph>
        </div>
      </div>
    </div>
  );
}
