import Head from 'next/head'
import Link from 'next/link'
import styles from '@/styles/Home.module.css'

export default function Home() {
  return (
    <>
      <Head>
        <title>Shot Selector - Home</title>
        <meta name="description" content="Intelligent system for selecting optimal prompting strategies" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>

      <div className={styles.hero}>
        <h1>Welcome to Shot Selector</h1>
        <p>Intelligent system for selecting optimal prompting strategies</p>
        <Link href="/analyze" className={styles.ctaButton}>
          Try it Now
        </Link>
      </div>

      <div className={styles.features}>
        <div className={styles.featureCard}>
          <h3>Zero-Shot</h3>
          <p>Direct prompting without examples</p>
        </div>
        <div className={styles.featureCard}>
          <h3>One-Shot</h3>
          <p>Learning from a single example</p>
        </div>
        <div className={styles.featureCard}>
          <h3>Chain-of-Thought</h3>
          <p>Step-by-step reasoning approach</p>
        </div>
      </div>
    </>
  )
} 