<script lang="ts">
	import { RangeSlider } from '@skeletonlabs/skeleton';
	import { Table, tableMapperValues } from '@skeletonlabs/skeleton';
	import type { TableSource } from '@skeletonlabs/skeleton';

	// Parameters for the slider to select the number of results
	let number_results = 6;
	let min_num_results = 1;
	let max_num_results = 25;

	// Function to create the table from the data
	function get_table_from_data(sourceData: any[]) {
		let tableSimple: TableSource = {
			// A list of heading labels.
			head: ['Distance', 'Document', 'Sentence Number', 'Sentence Content'],
			// The data visibly shown in your table body UI.
			body: tableMapperValues(sourceData, [
				'distance',
				'document',
				'sentence_number',
				'content'
			]),
			// Optional: The data returned when interactive is enabled and a row is clicked.
			meta: tableMapperValues(sourceData, ['document_id', 'sentence_number'])
			// Optional: A list of footer labels.
			//foot: ['Total', '', '<code class="code">6</code>']
		};
		return tableSimple;
	}

	// Initialize table with empty data
	let sourceData: any[] = [];
	let tableSimple = get_table_from_data(sourceData);

	// Get similar sentences from API when the button is clicked
	// Show the results in the table
	async function get_similar_documents() {
		const sentence = (document.querySelector('textarea') as HTMLTextAreaElement)?.value;
		const results = await fetch(
			`/api/similar-sentences?sentence=${sentence}&number_results=${number_results}`
		);
		const resultsJson = await results.json();
		sourceData = resultsJson;
		tableSimple = get_table_from_data(sourceData);
		//console.log(resultsJson);
	}

	function open_sentence_view() {
		console.log('open sentence view');
	}
</script>

<div class="container mx-auto space-y-8 p-8">
	<h1 class="h1">Search for semantically similar sentences in the corpus:</h1>
	<textarea class="textarea" rows="4" placeholder="Enter your sentence here." />

	<div class="flex">
		<div class="grow">
			<RangeSlider
				name="range-slider"
				bind:value={number_results}
				min={min_num_results}
				max={max_num_results}
				step={1}
				ticked>
				<div class="flex items-center justify-between">
					<div class="font-bold">Show number of closest results</div>
					<div class="text-xs">{number_results} / {max_num_results}</div>
				</div>
			</RangeSlider>
		</div>
		<button type="button" class="btn variant-filled" on:click={() => get_similar_documents()}
			>Find Results</button
		>
	</div>

	<Table
		class="table-interactive"
		interactive={true}
		on:selected={() => open_sentence_view()}
		source={tableSimple}
	/>
</div>
