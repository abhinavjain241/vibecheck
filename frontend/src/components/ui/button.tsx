import React from 'react'

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'default' | 'outline' | 'ghost'
}

export const Button: React.FC<ButtonProps> = ({ children, variant = 'default', ...props }) => {
  const baseStyle = 'px-4 py-2 rounded'
  const variantStyles = {
    default: 'bg-blue-500 text-white',
    outline: 'border border-blue-500 text-blue-500',
    ghost: 'text-blue-500',
  }

  return (
    <button className={`${baseStyle} ${variantStyles[variant]}`} {...props}>
      {children}
    </button>
  )
}