import React from 'react'
import { TooltipProps } from 'recharts'

interface ChartContainerProps extends React.HTMLAttributes<HTMLDivElement> {
  config?: {
    [key: string]: {
      label: string;
      color: string;
    }
  }
}

export const ChartContainer: React.FC<ChartContainerProps> = ({ children, config, ...props }) => (
  <div {...props}>{children}</div>
)

export const ChartTooltip: React.FC<TooltipProps> = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    return (
      <div className="bg-white p-2 border border-gray-200 shadow-md">
        <p>{`${label} : ${payload[0].value}`}</p>
      </div>
    )
  }
  return null
}

export const ChartTooltipContent = ChartTooltip