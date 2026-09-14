import { NavBar } from '@/components/NavBar'
import { Hero } from '@/sections/Hero'
import { SocialProof } from '@/sections/SocialProof'
import { ValuePillars } from '@/sections/ValuePillars'
import { CodeShowcase } from '@/sections/CodeShowcase'
import { Features } from '@/sections/Features'
import { Performance } from '@/sections/Performance'
import { Research } from '@/sections/Research'
import { Install } from '@/sections/Install'
import { CTA } from '@/sections/CTA'
import { Footer } from '@/sections/Footer'

export default function App() {
  return (
    <div className="min-h-screen overflow-x-hidden bg-bg">
      <NavBar />
      <main>
        <Hero />
        <SocialProof />
        <ValuePillars />
        <CodeShowcase />
        <Features />
        <Performance />
        <Research />
        <Install />
        <CTA />
      </main>
      <Footer />
    </div>
  )
}
