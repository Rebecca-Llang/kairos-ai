import * as React from 'react';
import { Slot } from '@radix-ui/react-slot';
import { cva, type VariantProps } from 'class-variance-authority';

import { cn } from '@/lib/utils';

const buttonVariants = cva(
  'inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg]:size-4 [&_svg]:shrink-0',
  {
    variants: {
      variant: {
        default:
          'bg-user-message hover:bg-indigo-950 text-message-text shadow-glow hover:shadow-glow-lg',
        destructive: 'bg-red-600 text-white shadow-sm hover:bg-red-700',
        outline:
          'border border-gray-700 bg-dark-matter hover:bg-stardust text-starlight hover:border-nebula',
        secondary:
          'bg-dark-matter hover:bg-stardust text-starlight border border-gray-700 hover:border-nebula',
        ghost: 'hover:bg-stardust hover:text-starlight',
        link: 'text-nebula underline-offset-4 hover:underline',
      },
      size: {
        default: 'h-10 sm:h-9 px-4 py-2 min-h-[44px]',
        sm: 'h-9 sm:h-8 rounded-md px-3 text-xs min-h-[44px] sm:min-h-[32px]',
        lg: 'h-12 sm:h-10 rounded-md px-8 min-h-[44px]',
        icon: 'h-10 w-10 sm:h-9 sm:w-9 min-h-[44px] min-w-[44px]',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'default',
    },
  }
);

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean;
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : 'button';
    return (
      <Comp
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    );
  }
);
Button.displayName = 'Button';

export { Button, buttonVariants };
